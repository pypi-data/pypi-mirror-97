import base64
import importlib
import io
from typing import Optional, List

import pkg_resources
import requests
import yaml
from packaging import version

from kikyo import Kikyo
from kikyo.utils import install_package


def configure_by_consul(config_url: str) -> Kikyo:
    """从Consul拉取YAML格式的配置文件

    :param config_url: 获取配置项的URL地址
    """

    resp = requests.get(config_url)
    resp.raise_for_status()

    ver = pkg_resources.get_distribution('kikyo').version
    since: Optional[str] = None
    conf = None
    for data in resp.json():
        v = data['Value']
        if not v:
            continue
        s = base64.b64decode(v)
        _conf: dict = yaml.safe_load(io.BytesIO(s))
        _since = _conf.get('since', '0')

        if since is None or version.parse(ver) >= version.parse(_since) > version.parse(since):
            since = _since
            conf = _conf

    if conf is None:
        raise RuntimeError('Configuration not found')

    plugins: Optional[List[dict]] = conf.get('plugins')
    if plugins:
        for kwargs in plugins:
            install_package(**kwargs)
    importlib.reload(pkg_resources)

    settings: dict = conf.get('kikyo')
    return Kikyo(settings)
