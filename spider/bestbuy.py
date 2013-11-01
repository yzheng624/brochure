from spider_base import BaseSpider
import re
from premix import ProductQuery
import requests


class BestBuySpider(BaseSpider):
    def __init__(self):
        BaseSpider.__init__(self)
        self.api_key = '5q7nvwnwfm5bc9xk7qbgb3gb'

    def run(self):
        pass

    def query(self, url):
        p = {}
        r = requests.get(url, headers=self.headers)
        html = r.content
        price = re.findall(r'<span class="price">\$([\d.]+)</span>', html)
        name = re.findall(r'<meta property="og:title" content="(.+)"/>', html)
        p['name'] = name[0]
        p['current_price'] = price[0]
        p['original_price'] = price[1]
        return p

    def get_sku(self, product_url):
        sku = int(re.findall(r'skuId=(\d+)&', product_url)[0])
        return sku

    def get_pid(self, product_url):
        pid = int(re.findall(r'id=(\d+)&', product_url)[0])
        return pid

if __name__ == '__main__':
    u = 'http://www.bestbuy.com/site/duke-nukem-forever-windows/2435079.p?id=1218328201673&skuId=2435079&strId=1436&strClr=true&ld=39.42216&lg=-76.78031&rd=25'
    b = BestBuySpider()
    print b.query(u)
