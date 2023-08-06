import atexit
import inspect
import json
import logging
import random
import re
import threading
import time
import traceback
import sys
from importlib import import_module

import requests
from qg_eureka import EurekaClient
from qg_tool.tool import get_host_ip

log = logging.getLogger('bootstrap')


def is_config(obj):
    try:
        json.dumps(obj)
        return True
    except:
        return False


config = {}
bootstrap = import_module('bootstrap')

for member in inspect.getmembers(bootstrap, is_config):
    config[member[0]] = member[1]


def init_arg(name, default):
    if config.get(name, None) is not None:
        pass
    else:
        config[name] = default
    return config[name]


profile = init_arg('profile', 'dev' if '--debug' in sys.argv else 'prod')
extra_profiles = init_arg('extra_profiles', 'logger')
if not re.search(r'(^|(?<=,))logger($|(?=,))', extra_profiles):
    extra_profiles = extra_profiles + ',logger'
    config.update(extra_profiles=extra_profiles)
ip = init_arg('ip', get_host_ip())
port = init_arg('port', 5000)
auto_load = init_arg('auto_load', True)

config_server_name = config['config_server_name']
app_name = config['app_name']
eureka_url = config['eureka_url']
eureka_heart = config['eureka_heart']

eureka = EurekaClient(app_name=app_name, port=port, ip_addr=ip,
                      eureka_url=eureka_url)


is_fail = False
stop = False


def register_eureka():

    def deregister():
        global stop
        stop = True
        eureka.deregister()

    def heart():
        global is_fail
        global stop
        while not stop:
            time.sleep(
                int(eureka_heart) if eureka_heart is not None and eureka_heart != '' else 20)
            try:
                eureka.renew()
                if is_fail:
                    log.info("eureka连接恢复")
                    is_fail = False
                log.debug('eureka renew')
                continue
            except:
                log.warning(f'连不上eureka: {eureka_url}')
                is_fail = True
                log.error(traceback.format_exc())
            finally:
                break
        if not stop:
            atexit.unregister(deregister)
            register_eureka()

    try:
        eureka.register()
        atexit.register(deregister)
    except:
        log.error(traceback.format_exc())
        register_eureka()
        return
    heart_thread = threading.Thread(target=heart, daemon=True)
    heart_thread.start()


def get_app_homepage(name, **kwargs):
    app = eureka.get_app(name)
    if not app:
        return None
    config_instances = app['application']['instance']
    config_instance = random.choice(config_instances)
    log.debug('调度服务 {} 地址 {}'.format(name, config_instance['homePageUrl']))
    return config_instance['homePageUrl']


def load_config():
    start = time.time()
    print('加载配置中...')
    config_app = eureka.get_app(config_server_name)
    config_instances = config_app['application']['instance']
    config_instance = random.choice(config_instances)
    url = '{homepage}{app_name}-{profile}{extra_profiles}.json'.format(
        homepage=config_instance['homePageUrl'], app_name=app_name, profile=profile,
        extra_profiles=f',{extra_profiles}' if extra_profiles else '')

    settings = requests.get(url).json()
    config.update(settings)
    with open('config.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(config, ensure_ascii=False,
                           indent=4, separators=(',', ':')))

    end = time.time()

    print('加载配置成功,耗时 %.2f s' % (end - start))
    if config.get('register', False):
        register_eureka()


if auto_load:
    load_config()
