from abc import ABCMeta, abstractmethod
from typing import Any, List, Optional


class Query(metaclass=ABCMeta):
    """构建面向topic的查询
    """

    @abstractmethod
    def select(self, name: str) -> 'FilterBuilder':
        """基于筛选表达式检索数据

        :param name: 筛选的字段名称
        """

    @abstractmethod
    def any(self) -> 'FilterBuilder':
        """面向任意字段筛选数据
        """

    @abstractmethod
    def nested(self, name: str, query: 'Query') -> 'Query':
        """嵌套查询

        :param name: 字段名称
        :param query: 查询
        """

    @abstractmethod
    def paginate(self, page: int = 0, size: int = 10) -> 'Query':
        """分页查询

        :param page: 分页的页码，从0开始
        :param size: 分页的大小
        """

    @abstractmethod
    def all(self) -> List[dict]:
        """返回命中查询的所有数据，默认进行了分页。
        """

    @abstractmethod
    def first(self) -> Optional[dict]:
        """返回命中查询的第一条数据
        """

    @abstractmethod
    def count(self) -> int:
        """返回命中查询的数据量
        """


class Index(metaclass=ABCMeta):
    """索引
    """

    @abstractmethod
    def exists(self, id: str) -> bool:
        """指定ID的数据是否存在

        :param id: 数据ID
        """

    @abstractmethod
    def get(self, id: str) -> dict:
        """返回指定数据

        :param id: 数据的ID
        """

    @abstractmethod
    def put(self, id: str, data: dict):
        """更新指定数据，指定ID不存在时自动创建数据

        :param id: 数据ID
        :param data: 数据内容
        """

    @abstractmethod
    def delete(self, id: str):
        """删除指定数据

        :param id: 数据ID
        """


class FilterBuilder(metaclass=ABCMeta):
    @abstractmethod
    def is_(self, value: Any) -> Query:
        """是某个值

        :param value: 具体值
        """

    @abstractmethod
    def is_not(self, value: Any) -> Query:
        """不是某个值

        :param value: 具体值
        """

    @abstractmethod
    def is_one_of(self, *values: Any) -> Query:
        """是其中某个值

        :param values: 具体值的列表
        """

    @abstractmethod
    def is_not_one_of(self, *values: Any) -> Query:
        """不是是其中某个值

        :param values: 具体值的列表
        """

    @abstractmethod
    def is_between(self, lower_bound: Any = None, upper_bound: Any = None) -> Query:
        """在区间范围内

        :param lower_bound: 最低值
        :param upper_bound: 最高值
        """

    @abstractmethod
    def is_not_between(self, lower_bound: Any = None, upper_bound: Any = None) -> Query:
        """不在区间范围内

        :param lower_bound: 最低值
        :param upper_bound: 最高值
        """

    @abstractmethod
    def exists(self) -> Query:
        """字段存在记录
        """

    @abstractmethod
    def does_not_exists(self) -> Query:
        """字段不存在记录
        """


class SearchClient(metaclass=ABCMeta):
    """
    提供全文检索服务
    """

    @abstractmethod
    def query(self, topic: str) -> Query:
        """
        对指定topic构建查询

        :param topic: topic名称
        """

    @abstractmethod
    def index(self, topic: str) -> Index:
        """
        对指定topic返回索引

        :param topic: topic名称
        """
