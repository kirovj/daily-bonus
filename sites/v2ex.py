import re
from datetime import datetime, date

import requests
from fake_useragent import UserAgent
from registry import register
from lxml import html


@register
class V2ex:

    def __init__(self):
        with open('cookies/v2ex.cookie', 'r') as f:
            self.cookie = f.read()
        self.s = requests.session()
        ua = UserAgent(platforms='desktop')
        self.headers = {
            'User-Agent': ua.random,
            'Referer': 'https://www.v2ex.com/',
            'Cookie': self.cookie
        }
        self.proxies = {"http": "http://127.0.0.1:7890"}
        self.once = None

    def _get(self, url: str):
        return self.s.get(url, headers=self.headers, proxies=self.proxies)

    def login(self) -> bool:
        r = self._get('https://www.v2ex.com/mission/daily')
        if r.ok:
            response = r.text
            if '你要查看的页面需要先登录' in response:
                return False
            match = re.search(r"once=(\d+)", r.text)
            if match:
                self.once = match.group(1)
                return True
        return False

    def bonus(self) -> (bool, str):
        self._get(f'https://www.v2ex.com/mission/daily/redeem?once={self.once}')
        r = self._get('https://www.v2ex.com/balance')
        tree = html.fromstring(r.content)
        checkin_day_str = tree.xpath('//small[@class="gray"]/text()')[0]
        checkin_day = datetime.now().astimezone().strptime(checkin_day_str, '%Y-%m-%d %H:%M:%S %z')
        if checkin_day.date() == date.today():
            bonus = re.search(r'\d+ 的每日登录奖励 (\d+ 铜币)', r.text)[1]
            balance = tree.xpath('//div[@class="balance_area bigger"]/text()')
            if len(balance) == 2:
                balance = ['0'] + balance
            golden, silver, bronze = [s.strip() for s in balance]
            return True, f'Earned {bonus}, {golden} 金币 {silver} 银币 {bronze} 铜币'
        else:
            return False, 'not found 每日登录奖励'
