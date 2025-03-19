import requests
import json
from mcdreforged.api.all import *

class Hitokoto:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def get_hitokoto(self, from_where: bool):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            data = json.loads(response.text)
            mes = build(data, from_where)
            return mes
        else:
            ServerInterface.get_instance().logger.error(f"Failed to get hitokoto from {self.api_url}.Error code: {response.status_code}")
            return None
        
def build(data: dict, if_from_where: bool) -> str:
    message = data['hitokoto']
    from_where = data['from']
    if if_from_where:
        message += f"——{from_where}"
    return message

    
if __name__ == '__main__':
    hitokoto = Hitokoto("https://v1.hitokoto.cn/")
    print(hitokoto.get_hitokoto(False))