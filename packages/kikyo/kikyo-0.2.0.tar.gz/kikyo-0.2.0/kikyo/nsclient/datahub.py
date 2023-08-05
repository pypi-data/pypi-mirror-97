from abc import ABCMeta, abstractmethod
from typing import Any


class Producer(metaclass=ABCMeta):
    """生产者
    """

    def __enter__(self) -> 'Producer':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @abstractmethod
    def send(self, *records: Any):
        """发送数据

        :param records: 数据
        """

    @abstractmethod
    def close(self):
        """关闭生产者
        """


class Message(metaclass=ABCMeta):
    """消息
    """

    @property
    @abstractmethod
    def value(self) -> Any:
        """消息内容
        """


class Consumer(metaclass=ABCMeta):
    """
    消费者
    """

    def __enter__(self) -> 'Consumer':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @abstractmethod
    def receive(self) -> Message:
        """接收数据
        """

    @abstractmethod
    def close(self):
        """关闭消费者
        """


class DataHubClient(metaclass=ABCMeta):
    """提供数据总线服务
    """

    @abstractmethod
    def create_producer(self, topic: str) -> Producer:
        """创建向指定topic发送数据的生产者

        :param topic: topic名称
        """

    @abstractmethod
    def subscribe(
            self,
            topic: str,
            subscription_name: str = None,
    ) -> Consumer:
        """订阅指定topic

        :param topic: topic名称
        :param subscription_name: 订阅的标识
        """
