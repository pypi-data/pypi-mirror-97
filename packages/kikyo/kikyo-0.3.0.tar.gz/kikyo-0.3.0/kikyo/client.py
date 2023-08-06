import pkg_resources

from kikyo.acl import AclService
from kikyo.nsclient.analytic import AnalyticClient
from kikyo.nsclient.datahub import DataHubClient
from kikyo.nsclient.objstore import ObjStoreClient
from kikyo.nsclient.search import SearchClient
from kikyo.settings import Settings


class Kikyo:
    datahub: DataHubClient
    objstore: ObjStoreClient
    search: SearchClient
    analytic: AnalyticClient

    acl: AclService
    settings: Settings

    def __init__(self, settings: dict = None):
        if settings is not None:
            self.init(settings)

    def init(self, settings) -> 'Kikyo':
        self.settings = Settings(settings)
        self._init_plugins()
        return self

    def _init_plugins(self):
        plugins = {
            entry_point.name: entry_point.load()
            for entry_point in pkg_resources.iter_entry_points('kikyo.plugins')
        }

        active_plugins = self.settings.getlist('active_plugins')
        if active_plugins:
            active_plugins = set(active_plugins)
            for name in list(plugins.keys()):
                if name not in active_plugins:
                    del plugins[name]

        for name, plugin in plugins.items():
            if hasattr(plugin, 'configure_kikyo'):
                plugin.configure_kikyo(self)

    def login(self, access_key: str, secret_key: str) -> 'Kikyo':
        """用户登录

        :param access_key: 用户名
        :param secret_key: 密码
        """
        self.acl.login(access_key, secret_key)
        return self
