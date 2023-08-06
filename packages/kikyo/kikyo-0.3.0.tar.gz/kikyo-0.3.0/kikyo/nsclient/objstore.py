from abc import ABCMeta, abstractmethod
from typing import Any


class Bucket(metaclass=ABCMeta):
    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def get_object_link(self, key: str) -> str:
        """获取文件的下载链接

        :param key: 文件的名称
        """

    @abstractmethod
    def put_object(self, key: str, data: Any):
        """上传文件

        :param key: 文件的名称
        :param data: 文件数据
        """


class ObjStoreClient(metaclass=ABCMeta):
    """提供文件存储服务
    """

    @abstractmethod
    def bucket(self, name: str) -> Bucket:
        """获取bucket

        :param name: bucket名称
        """
