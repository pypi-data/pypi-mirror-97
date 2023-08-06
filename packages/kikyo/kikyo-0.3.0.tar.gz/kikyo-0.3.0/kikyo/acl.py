from abc import ABCMeta, abstractmethod
from enum import Enum


class AclPerm(Enum):
    read = 1
    write = 2
    full = 3


class AclService(metaclass=ABCMeta):

    @abstractmethod
    def login(self, access_key: str, secret_key: str):
        """用户登录

        :param access_key: 用户名
        :param secret_key: 密码
        """

    @abstractmethod
    def has_permission(self, resource: str, permission: AclPerm) -> bool:
        """检查是具有对资源的访问权限

        :param resource: 资源名称
        :param permission: 权限
        """
