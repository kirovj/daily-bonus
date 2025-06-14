import importlib
import pkgutil

import sites
from registry import site_list
from logger import logger


def auto_import_sites(package):
    for _, modname, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{package.__name__}.{modname}")


def run_all():
    for site in site_list:
        site_name = site.__class__.__name__
        log = logger.bind(key=site_name)
        log.info('start daily bonus')
        if site.login():
            log.success('login success! try bonus...')
            is_success, message = site.bonus()
            if is_success:
                log.success(f'Bonus success! {message}')
            else:
                log.warning(f'Bonus fail! {message}')


if __name__ == "__main__":
    auto_import_sites(sites)
    run_all()
