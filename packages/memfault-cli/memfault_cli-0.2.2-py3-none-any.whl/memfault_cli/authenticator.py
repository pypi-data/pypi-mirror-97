from abc import abstractmethod
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from memfault_cli.context import MemfaultCliClickContext


class Authenticator:
    def __init__(self, ctx: "MemfaultCliClickContext"):
        self.ctx = ctx

    @classmethod
    def create_authenticator_given_context_or_raise(cls, ctx: "MemfaultCliClickContext"):
        """
        Given a CLI context, determine which auth system to use.
        Simple implementation for now. If this becomes more complicated, iterate through
        subclasses instead.
        """
        if ctx.obj.get("project_key"):
            return ProjectKeyAuthenticator(ctx)
        else:
            return BasicAuthenticator(ctx)

    @staticmethod
    @abstractmethod
    def project_key_auth() -> bool:
        pass

    @staticmethod
    @abstractmethod
    def required_args() -> List[str]:
        pass

    @abstractmethod
    def requests_auth_params(self) -> dict:
        pass


class ProjectKeyAuthenticator(Authenticator):
    """
    Project Key Authentication with the Memfault service (Memfault-Project-Key)
    """

    @staticmethod
    def project_key_auth() -> bool:
        return True

    @staticmethod
    def required_args() -> List[str]:
        return [
            "project_key",
        ]

    def requests_auth_params(self) -> dict:
        return dict(headers={"Memfault-Project-Key": self.ctx.project_key})


class BasicAuthenticator(Authenticator):
    """
    Basic Authentication with the Memfault service

    Various ways a user can authenticate:
    - Email + Password
    - Email + User API Key
    - Organization Auth Token (passed in as password)
    """

    @staticmethod
    def project_key_auth() -> bool:
        return False

    @staticmethod
    def required_args() -> List[str]:
        return [
            "org",
            "project",
            "password",
        ]

    def requests_auth_params(self) -> dict:
        # Email can be None in the case of using Organization auth tokens (prefixed with oat_*)
        auth = (self.ctx.obj.get("email") or "", self.ctx.password)
        return dict(auth=auth)
