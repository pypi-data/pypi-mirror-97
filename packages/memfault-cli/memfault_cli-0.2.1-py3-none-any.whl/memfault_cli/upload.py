import hashlib
import logging
import os
import re
import urllib
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor
from glob import glob
from typing import IO, Any, Dict, Generator, Optional, Tuple, Type
from zipfile import is_zipfile

import click
import requests
from elftools.elf.elffile import ELFFile
from requests import Response, Session
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
from urllib3 import Retry

from . import functools_ext
from .authenticator import Authenticator
from .context import MemfaultCliClickContext, PackageInfo
from .gnu_build_id import get_gnu_build_id

LOG = logging.getLogger(__name__)

GNU_BUILD_ID_RE = re.compile(r"Build ID: (?P<gnu_build_id>[a-f\d]+)")


def hash_io_hexdigest(name, data: IO, chunksize=2 ** 20) -> str:
    """
    A wrapper around hashlib.new() and hexdigest() which reads
    from a stream in chunks
    """
    assert data.readable()

    # In case it's a large file, read it in chunks.
    h = hashlib.new(name)
    while True:
        chunk = data.read(chunksize)
        if not chunk:
            break
        h.update(chunk)
    return h.hexdigest()


def check_response(response: Response):
    if response.status_code >= 400:
        raise Exception(
            f"Request failed with HTTP status {response.status_code}\nResponse body:\n{response.content.decode()}"
        )


def url_quote(value: str) -> str:
    return urllib.parse.quote(value, safe="", encoding="utf-8")


class Uploader:
    def __init__(
        self, *, ctx: MemfaultCliClickContext, file_path: str, authenticator: Authenticator
    ):
        self.ctx: MemfaultCliClickContext = ctx
        self.file_path = file_path
        self.authenticator: Authenticator = authenticator
        self.session = self._create_requests_session()

    @staticmethod
    def _create_requests_session() -> Session:
        retry_strategy = Retry(
            total=5,
            backoff_factor=2,  # Sleep for 2s, 4s, 8s, 16s, 32s, Stop
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "POST", "PUT"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    @staticmethod
    @abstractmethod
    def project_key_auth() -> bool:
        pass

    @property
    def base_url(self):
        return self.ctx.file_url

    @property
    def app_url(self):
        return self.ctx.app_url

    def _api_base_url(self) -> str:
        return f"{self.base_url}/api/v0"

    def _projects_base_url(self) -> str:
        return f"{self.base_url}/api/v0/organizations/{self.ctx.org}/projects/{self.ctx.project}"

    def _projects_ui_base_url(self) -> str:
        return f"{self.app_url}/organizations/{self.ctx.org}/projects/{self.ctx.project}"

    def upload_url(self) -> str:
        """
        The upload URL for a 'prepared upload' for the configured authentication method.
        """
        if self.authenticator.project_key_auth():
            return f"{self._api_base_url()}/upload"
        else:
            return f"{self._projects_base_url()}/upload"

    @abstractmethod
    def can_upload_file(self) -> bool:
        """Test the file pointed to by `file_path`."""
        pass

    @abstractmethod
    def entity_url(self) -> str:
        """The final URL to POST to during the prepared upload sequence."""
        pass

    def ui_url(self) -> Optional[str]:
        """The UI URL at which results from the operation can be seen"""
        return None

    @abstractmethod
    def requests_auth_params(self) -> dict:
        """A dict of `requests` parameters that should be used for authentication."""
        pass

    def _is_already_uploaded(self) -> bool:
        return False

    def _prepare_upload(self) -> Tuple[str, str]:
        response = self.session.post(self.upload_url(), **self.authenticator.requests_auth_params())
        check_response(response)
        data = response.json()["data"]
        return data["upload_url"], data["token"]

    def _put_file(self, upload_url: str, *, progressbar=True) -> None:
        file_size = os.stat(self.file_path).st_size
        with open(self.file_path, "rb") as file:
            with tqdm(
                total=file_size,
                desc=os.path.basename(file.name),
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                disable=not progressbar,
            ) as t:
                wrapped_file = CallbackIOWrapper(t.update, file, "read")
                response = self.session.put(upload_url, data=wrapped_file)
                check_response(response)

    def post_token_extra_request_data(self) -> Optional[Dict]:
        return None

    def _post_token(self, token: str) -> None:
        json_d = {
            "file": {"token": token, "md5": self.file_md5, "name": self.file_basename},
        }
        extra_request_data = self.post_token_extra_request_data()
        if extra_request_data:
            json_d.update(extra_request_data)
        check_response(
            self.session.post(
                self.entity_url(), json=json_d, **self.authenticator.requests_auth_params()
            )
        )

    def _is_elf(self) -> bool:
        with open(self.file_path, "rb") as file:
            if file.read(4) != b"\x7FELF":
                return False

        return True

    def _get_gnu_build_id_and_has_debug_info(self) -> Tuple[Optional[str], bool]:
        with open(self.file_path, "rb") as f:
            elf = ELFFile(f)
            return get_gnu_build_id(elf), elf.has_dwarf_info()

    def upload(self, *, progressbar=True) -> bool:
        if self._is_already_uploaded():
            LOG.info(f"{self.file_path}: skipping, already uploaded.")
            return False
        upload_url, token = self._prepare_upload()
        self._put_file(upload_url, progressbar=progressbar)
        self._post_token(token)
        LOG.info(f"{self.file_path}: uploaded!")
        if self.ui_url():
            click.echo(f"You can view in the UI here:\n   {self.ui_url()}")
        return True

    @functools_ext.cached_property
    def file_md5(self):
        with open(self.file_path, "rb") as f:
            return hash_io_hexdigest("md5", f)

    @property
    def file_basename(self):
        return os.path.basename(self.file_path)


class BugreportUploader(Uploader):
    def can_upload_file(self) -> bool:
        if not is_zipfile(self.file_path):
            LOG.error(f"{self.file_path} is not a valid zip file!")
            return False
        return True

    def entity_url(self) -> str:
        if self.authenticator.project_key_auth():
            return f"{self._api_base_url()}/upload/bugreport"
        else:
            return f"{self._projects_base_url()}/bugreports"


class CoredumpUploader(Uploader):
    def can_upload_file(self) -> bool:
        with open(self.file_path, "rb") as f:
            hdr = f.read(4).decode("ascii", errors="ignore")
            if hdr != "CORE":
                LOG.error(f"{self.file_path} is not a Memfault Coredump")
                return False

        return True

    def entity_url(self) -> str:
        if self.authenticator.project_key_auth():
            return f"{self._api_base_url()}/upload/coredump"
        else:
            return f"{self._projects_base_url()}/coredumps"


class SymbolUploader(Uploader):
    gnu_build_id: str = ""

    def can_upload_file(self) -> Optional[Any]:
        if not self._is_elf():
            LOG.info(f"{self.file_path}: Not an ELF file")
            return False

        self.gnu_build_id, has_debug_info = self._get_gnu_build_id_and_has_debug_info()
        if not self.gnu_build_id:
            LOG.info(f"{self.file_path}: looks like an ELF but does not contain a GNU Build ID")
            return False
        if not has_debug_info:
            LOG.info(f"{self.file_path}: looks like an ELF but it has no .debug_info")
            return False
        LOG.info(
            f"{self.file_path}: ELF file with .debug_info and GNU Build ID: {self.gnu_build_id}"
        )
        return True

    def _is_already_uploaded(self) -> bool:
        response = self.session.head(
            f"{self._projects_base_url()}/symbols-by-gnu-build-id/{self.gnu_build_id}",
            **self.authenticator.requests_auth_params(),
        )
        try:
            check_response(response)
        except Exception:
            if response.status_code == 404:
                return False
            raise
        return True

    def entity_url(self) -> str:
        return f"{self._projects_base_url()}/symbols"


class SoftwareArtifactUploader(Uploader):
    def can_upload_file(self) -> Optional[Any]:
        if not self._is_elf():
            LOG.info(f"{self.file_path}: Not an ELF file")
            return False

        self.gnu_build_id, has_debug_info = self._get_gnu_build_id_and_has_debug_info()
        if not self.gnu_build_id:
            # We can handle a symbol artifact without a Build ID but might as well
            # recommend it!
            LOG.info(
                f"{self.file_path}: Consider adding a GNU Build ID to uniquely identify the build"
            )

        if not has_debug_info:
            LOG.info(f"{self.file_path}: looks like an ELF but it has no .debug_info")
            return False
        LOG.info(f"{self.file_path}: ELF file with .debug_info")
        return True

    def _is_already_uploaded(self) -> bool:
        return False

    def entity_url(self) -> str:
        return f"{self._projects_base_url()}/symbols"

    def ui_url(self) -> str:
        software_type = url_quote(self.ctx.software_info.software_type)
        software_version = url_quote(self.ctx.software_info.software_version)
        return (
            f"{self._projects_ui_base_url()}/software/{software_type}/versions/{software_version}"
        )

    def post_token_extra_request_data(self) -> Optional[Dict]:
        info = self.ctx.software_info
        return {
            "software_version": {
                "version": info.software_version,
                "software_type": info.software_type,
                **({"revision": info.revision} if info.revision else {}),
            },
        }

    @staticmethod
    def project_key_auth() -> bool:
        return False


class ReleaseArtifactUploader(Uploader):
    def can_upload_file(self) -> Optional[Any]:
        # There are no restrictions for the type of binary a customer uses for
        # a release
        return True

    def _is_already_uploaded(self) -> bool:
        return False

    def entity_url(self) -> str:
        return f"{self._projects_base_url()}/releases/ota_payload"

    def ui_url(self) -> str:
        software_version = url_quote(self.ctx.software_info.software_version)
        return f"{self._projects_ui_base_url()}/releases/{software_version}"

    def post_token_extra_request_data(self) -> Optional[Dict]:
        info = self.ctx.software_info

        return {
            "software_version": {
                "version": info.software_version,
                "software_type": info.software_type,
                **({"revision": info.revision} if info.revision else {}),
            },
            "must_pass_through": self.ctx.must_pass_through,
            "hardware_version": self.ctx.hardware_version,
        }


class DirectoryUploader(Uploader):
    uploader_cls: Type[Uploader] = None

    def can_upload_file(self) -> bool:
        return os.path.isdir(self.file_path)

    def _walk_files(self, root: str) -> Generator[str, Any, Any]:
        for root, _dirs, files in os.walk(root):
            yield from map(lambda file: os.path.join(root, file), files)

    def upload(self, *, progressbar=True) -> bool:
        queued_uploaders = []
        did_upload = False

        for file_path in self._walk_files(self.file_path):
            uploader = self.uploader_cls(
                ctx=self.ctx, file_path=file_path, authenticator=self.authenticator
            )
            if uploader.can_upload_file():
                queued_uploaders.append(uploader)
                did_upload |= True
            else:
                LOG.info(f"{file_path}: skipping...")

        def do_upload(uploader: Uploader):
            uploader.upload(progressbar=False)

        # If we find that we have more implementations that need to do parallel uploads,
        # We should generalize this logic into a class or have a function called `get_uploaders`
        # that the calling client can then parallelize by calling `.upload()` on each.
        with ThreadPoolExecutor(max_workers=self.ctx.concurrency) as pool:
            # NB: We need to read the result for exceptions to be raised
            for result in pool.map(do_upload, queued_uploaders):
                del result

        return did_upload


class SymbolDirectoryUploader(DirectoryUploader):
    uploader_cls = SymbolUploader


class ProguardMappingUploader(Uploader):
    def __init__(
        self,
        *,
        ctx: MemfaultCliClickContext,
        file_path: str,
        authenticator: Authenticator,
        package_info: PackageInfo,
    ):
        super().__init__(ctx=ctx, file_path=file_path, authenticator=authenticator)
        self.package_info = package_info

    def can_upload_file(self) -> Optional[Any]:
        return True

    def entity_url(self) -> str:
        return f"{self._projects_base_url()}/symbols"

    def post_token_extra_request_data(self) -> Optional[Dict]:
        return {
            "software_version": {
                "version": f"{self.package_info.version_name}:{self.package_info.version_code}",
                "software_type": self.package_info.name,
            },
        }


class AndroidAppSymbolsUploader(Uploader):
    def can_upload_file(self) -> bool:
        if not os.path.isdir(self.file_path):
            LOG.error(
                f'{self.file_path} is not a directory. Please specify the Android app\'s root "build" path instead!'
            )
            return False
        return True

    def _find_apk_path(self) -> str:
        apk_dir = os.path.join(self.file_path, "outputs", "apk", self.ctx.build_variant)
        if not os.path.isdir(apk_dir):
            raise click.exceptions.FileError(
                apk_dir, hint='Please pass the Android app\'s root "build" path!'
            )
        apk_glob = os.path.join(apk_dir, "*.apk")
        apks = glob(apk_glob)
        if not apks:
            raise click.exceptions.FileError(apk_glob, hint="No .apk found!")
        if len(apks) > 1:
            raise click.exceptions.FileError(apk_glob, hint="Multiple .apks found!")
        return apks[0]

    def _get_package_info_from_apk(self) -> PackageInfo:
        from pyaxmlparser import APK

        apk = APK(self._find_apk_path())
        return PackageInfo(apk.get_package(), apk.version_name, apk.version_code)

    def _find_mapping_txt(self) -> Optional[str]:
        if self.ctx.android_mapping_txt:
            return self.ctx.android_mapping_txt
        # In older version, the default folder was called "proguard", later it got renamed to "mapping":
        subdirs = ("mapping", "proguard")
        paths_to_check = tuple(
            map(
                lambda subdir: os.path.join(
                    self.file_path, "outputs", "mapping", self.ctx.build_variant, "mapping.txt"
                ),
                subdirs,
            )
        )
        for path in paths_to_check:
            if os.path.isfile(path):
                return path
        LOG.info("No mapping.txt found in default locations, assuming ProGuard/R8 is disabled...")
        return None

    def _upload_mapping_txt(self) -> bool:
        mapping_txt_path = self._find_mapping_txt()
        if not mapping_txt_path:
            return False
        package_info = self.ctx.android_package_info
        if not package_info:
            package_info = self._get_package_info_from_apk()
        pg_uploader = ProguardMappingUploader(
            ctx=self.ctx,
            file_path=mapping_txt_path,
            package_info=package_info,
            authenticator=self.authenticator,
        )
        return pg_uploader.upload()

    def _upload_ndk_symbols(self) -> bool:
        # TODO: add support for legacy ndkBuild?
        cmake_path_out = os.path.join(
            self.file_path, "intermediates", "cmake", self.ctx.build_variant
        )
        if not os.path.isdir(cmake_path_out):
            return False
        sym_dir_uploader = SymbolDirectoryUploader(
            ctx=self.ctx, file_path=cmake_path_out, authenticator=self.authenticator
        )
        return sym_dir_uploader.upload()

    def upload(self, *, progressbar=True) -> bool:
        did_upload = self._upload_mapping_txt() or self._upload_ndk_symbols()
        if not did_upload:
            raise click.exceptions.UsageError("No files uploaded!")
        return did_upload
