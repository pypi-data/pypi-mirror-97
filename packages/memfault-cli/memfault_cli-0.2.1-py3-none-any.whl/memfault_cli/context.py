from typing import Optional

import click
from memfault_cli.authenticator import Authenticator


class PackageInfo:  # noqa: B903 - no data classes in Python 3.6
    def __init__(self, name: str, version_name: str, version_code: str):
        self.name = name
        self.version_name = version_name
        self.version_code = version_code


class SoftwareInfo:  # noqa: B903 - no data classes in Python 3.6
    def __init__(self, software_type: str, software_version: str, revision: Optional[str] = None):
        self.software_type = software_type
        self.software_version = software_version
        self.revision = revision


class MemfaultCliClickContext(object):
    """
    A context passed around between the memfault cli sub-commands.


    If the top level CLI has any "required" it's not possible to display
    any help info about the subcommands using "--help" without providing them.
    By passing around this context, subcommand help messages can be displayed
    and errors can be raised in a uniform way
    """

    def __init__(self):
        self.obj = {}

    def _find_obj_or_raise(self, name):
        value = self.obj.get(name)
        if value is None:
            option = name.replace("_", "-")
            raise click.exceptions.UsageError(f'Missing option "--{option}".')
        return value

    def check_required_cli_args(self, *, authenticator: Authenticator):
        required_args = authenticator.required_args()

        for arg in required_args:
            self._find_obj_or_raise(arg)

    @property
    def org(self):
        return self._find_obj_or_raise("org")

    @property
    def project(self):
        return self._find_obj_or_raise("project")

    @property
    def email(self):
        return self._find_obj_or_raise("email")

    @property
    def password(self):
        return self._find_obj_or_raise("password")

    @property
    def project_key(self):
        return self._find_obj_or_raise("project_key")

    @property
    def concurrency(self):
        return self._find_obj_or_raise("concurrency")

    @property
    def software_info(self) -> Optional[SoftwareInfo]:
        sw_type = self.obj.get("software_type")
        sw_ver = self.obj.get("software_version")
        revision = self.obj.get("revision")
        if sw_type is None and sw_ver is None:
            return None

        if sw_type is None or sw_ver is None:
            raise click.exceptions.UsageError(
                '"--software-version" and "--software-type" must be specified together'
            )

        return SoftwareInfo(software_type=sw_type, software_version=sw_ver, revision=revision)

    @property
    def file_url(self) -> str:
        FILES_BASE_URL = "https://files.memfault.com"
        url = self.obj.get("url")
        if url is None:
            return FILES_BASE_URL
        return url

    @property
    def app_url(self) -> str:
        APP_BASE_URL = "https://app.memfault.com"
        url = self.obj.get("url")
        if url is None:
            return APP_BASE_URL
        return url

    @property
    def chunks_url(self) -> str:
        CHUNKS_BASE_URL = "https://chunks.memfault.com"
        url = self.obj.get("url")
        if url is None:
            return CHUNKS_BASE_URL
        return url

    @property
    def api_url(self) -> str:
        CHUNKS_BASE_URL = "https://api.memfault.com"
        url = self.obj.get("url")
        if url is None:
            return CHUNKS_BASE_URL
        return url

    @property
    def hardware_version(self):
        return self.obj.get("hardware_version", None)

    @property
    def device_serial(self):
        return self._find_obj_or_raise("device_serial")

    @property
    def build_variant(self):
        return self._find_obj_or_raise("build_variant")

    @property
    def must_pass_through(self):
        return self._find_obj_or_raise("must_pass_through")

    @property
    def android_package_info(self) -> Optional[PackageInfo]:
        package = self.obj.get("package")
        version_name = self.obj.get("version_name")
        version_code = self.obj.get("version_code")
        if package is None and version_name is None and version_code is None:
            return None
        if package is None or version_name is None or version_code is None:
            raise click.exceptions.UsageError(
                '"--package, --version-name" and "--version-code" must be specified together'
            )

        return PackageInfo(package, version_name, version_code)

    @property
    def android_mapping_txt(self) -> Optional[str]:
        return self.obj.get("mapping_txt")
