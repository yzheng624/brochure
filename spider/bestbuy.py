from spider_base import BaseSpider
import re
import requests
from brochure.models import *
from django.core.mail import send_mail


class BestBuySpider(BaseSpider):
    def __init__(self):
        BaseSpider.__init__(self)
        self.api_key = '5q7nvwnwfm5bc9xk7qbgb3gb'

    def run(self):
        products = Product.objects.filter(website='bestbuy')
        for product in products:
            print product.name
            print 'Before:' + str(product.current_price)
            p = self.query(product.url)
            if str(product.current_price) != str(p['current_price']):
                prev_price = product.current_price
                product.current_price = float(p['current_price'])
                product.save()
                watchlist = Watchlist.objects.filter(product__pk=product.pk)
                to_list = []
                for w in watchlist:
                    to_list.append(w.email)
                send_mail(product.name + '\'s price been updated', 'From ' + str(prev_price) + ' to ' + str(product.current_price), 'brochuredev@126.com', to_list, fail_silently=False)
                print 'After:' + str(product.current_price)

    def query(self, url):
        p = {}
        r = requests.get(url, headers=self.headers)
        html = r.content
        price = re.findall(r'price">(?:\$|<span class="denominator">\$</span>)([\d.,]+)(</span>|</div>)', html, re.DOTALL)
        name = re.findall(r'<meta property="og:title" content="(.*?)"/>', html, re.DOTALL)
        p['name'] = name[0].split('"')[0]
        p['current_price'] = price[0][0]
        # p['original_price'] = price[1][0]
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
