# -*- coding: utf-8 -*-
import re
from urllib.parse import urlencode
from mcdreforged.api.all import *
from hitokoto.getHitokoto import Hitokoto
import time
import json


def tr(key, *args):
    return ServerInterface.get_instance().tr(f"hitokoto.{key}", *args)

def command_register(server: ServerInterface):
    builder = SimpleCommandBuilder()
    builder.command('!!hitokoto', get_help)
    builder.command('!!hitokoto help', get_help)
    builder.command('!!hitokoto set <interval>', set_interval)
    builder.command('!!hitokoto start', start_auto_hitokoto)
    builder.command('!!hitokoto stop', stop_auto_hitokoto)
    builder.command('!!hitokoto status', get_status)
    builder.arg('interval', Text)
    builder.register(server)

class Config(Serializable):
    interval: str = "60s"
    base_url: str = "https://v1.hitokoto.cn/"
    parameters: dict = {}
    from_where: bool = False
    def save(self):
        global interval, base_url, parameters, from_where
        interval, parameters, base_url, from_where = get_config()
        dict_config = {
            "interval": self.interval,
            "parameters": self.parameters,
            "base_url": self.base_url,
            "from_where": self.from_where
        }
        with open('./config/hitokoto/config.json', 'w', encoding='utf-8') as f:
            json.dump(dict_config, f, ensure_ascii=False, indent=4)
    
FLAG = 0

interval = "60s"
base_url = "https://v1.hitokoto.cn/"
parameters = {}
from_where = False
config: Config

def on_load(server: PluginServerInterface, old):
    command_register(server)
    global config, interval, base_url, parameters, from_where
    config = server.load_config_simple(
        'config.json',
        target_class=Config
    )
    try:
        interval, parameters, base_url, from_where = get_config()
        
    except Exception as e:
        server.logger.error(tr('error.load_config_error'), e)
        interval = "60s"
        base_url = "https://v1.hitokoto.cn/"
        parameters = {}
        from_where = False
    auto_Hitokoto_thread()

def get_config():
    global config
    return config.interval, config.parameters, config.base_url, config.from_where


def build_url():
    global base_url, parameters
    if parameters:
        return f"{base_url}?{urlencode(parameters, doseq=True)}"
    else:
        return base_url
    
def get_hitokoto():
    global from_where
    url = build_url()
    hitokoto = Hitokoto(url)
    response = hitokoto.get_hitokoto(from_where)
    if response:
        return response
    else:
        return None
    
def parse_time_string() -> int:
    global interval, config
    time_units = {
        's': 1,
        'm': 60,
        'h': 3600
    }
    match = re.match(r'(\d+)([smh])', interval)
    if not match:
        ServerInterface.get_instance().logger.error(f"{tr('error.interval_too_short')}{interval}")
    number, unit = match.groups()
    interval_seconds = int(number) * time_units[unit]
    if interval_seconds < 10:
        interval_seconds = 10
        ServerInterface.get_instance().logger.error(f"{tr('error.interval_too_short')}: {interval}")
    return interval_seconds

@new_thread
def auto_Hitokoto_thread():
    global FLAG
    interval = parse_time_string()
    if interval < 10:
        FLAG = 0
        ServerInterface.get_instance().logger.error(f"{tr('error.interval_too_short')}: {interval}")
        return
    while FLAG == 1:
        time.sleep(interval)
        response = get_hitokoto()
        if response is not None:
            ServerInterface.get_instance().say(f"§a[Hitokoto] \n {response}")
        else:
            ServerInterface.get_instance().say(f"§c[Hitokoto] \n {tr('error.get_hitokoto_failed')}")

def get_help(source: CommandSource):
    source.reply(tr("help_message"))

def set_interval(source: CommandSource, context: CommandContext):
    global config
    config.interval = context['interval']
    source.reply(tr("set_interval_success")+config.interval)
    config.save()


def start_auto_hitokoto(source: CommandSource):
    global FLAG
    if FLAG == 0:
        FLAG = 1
        source.reply(tr("start_auto_hitokoto_success"))
        auto_Hitokoto_thread()
    else:
        source.reply(tr("auto_hitokoto_is_running"))

def stop_auto_hitokoto(source: CommandSource):
    global FLAG
    if FLAG == 1:
        FLAG = 0
        source.reply(tr("stop_auto_hitokoto_success"))
    else:
        source.reply(tr("auto_hitokoto_is_not_running"))

def get_status(source: CommandSource):
    global FLAG
    auto_hitokoto_is_running = "False"
    if FLAG == 1:
        auto_hitokoto_is_running = "True"
    source.reply(f"""
        Interval: {config.interval}\n
        Base url: {config.base_url}\n
        Parameters: {config.parameters}\n
        Total url: {build_url()}\n
        Auto Hitokoto is Running: {auto_hitokoto_is_running}\n
    """)
                
                