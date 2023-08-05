import pkg_resources
from packaging import version
from pip._internal.cli.main import main as pip_main


def install_package(pkg: str, min_ver: str = None, max_ver: str = None, index_url: str = None):
    def _check_pkg_version(pkg_ver):
        if min_ver and version.parse(pkg_ver) < version.parse(min_ver):
            return False
        if max_ver and version.parse(pkg_ver) >= version.parse(max_ver):
            return False
        return True

    try:
        _dist = pkg_resources.get_distribution(pkg)
        if _check_pkg_version(_dist.version):
            return
    except pkg_resources.DistributionNotFound:
        pass

    cmd = ['install']
    ver = []
    if min_ver:
        ver.append(f'>={min_ver}')
    if max_ver:
        ver.append(f'<{max_ver}')
    cmd.append(f'{pkg}{",".join(ver)}')
    if index_url:
        cmd.extend(['--index-url', index_url])
        cmd.extend(['--extra-index-url', 'https://pypi.org/simple'])
    pip_main(cmd)
