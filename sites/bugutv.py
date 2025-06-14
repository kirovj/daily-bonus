import re
import json

import requests
from fake_useragent import UserAgent
from registry import register


@register
class Bugutv:

    def __init__(self):
        with open('cookies/bugutv.json', 'r') as f:
            self.login_data = json.load(f)
        self.s = requests.session()
        ua = UserAgent(platforms='desktop')
        self.s.headers.update({
            'User-Agent': ua.random,
        })
        self.login_url = 'https://www.bugutv.vip/wp-admin/admin-ajax.php'
        self.nonce = None

    def login(self) -> bool:
        self.s.post(self.login_url, data=self.login_data)
        r = self.s.get('https://www.bugutv.vip/user')
        if r.ok and '每日签到' in r.text:
            match = re.search(r'<a class="user-logout".*?_wpnonce=([^"]+)', r.text)
            if match:
                self.nonce = match.group(1)
                return True
        return False

    def bonus(self) -> (bool, str, str):
        r = self.s.post(self.login_url, data={'action': 'user_qiandao', 'nonce': self.nonce})
        response = json.loads(r.content.decode('utf-8-sig'))
        status = response['status']
        msg = response['msg']
        if status == '1':
            r = self.s.get('https://www.bugutv.vip/user')
            match = re.search(r'当前余额：\d+', r.text)
            if match:
                balance = match.group(0)
                return True, f'{msg}, {balance}'
        return False, msg
