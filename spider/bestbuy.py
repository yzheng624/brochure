from spider_base import BaseSpider
import re
import requests
try:
    from brochure.models import *
except:
    pass
from django.core.mail import send_mail
from premix import ProductQuery
import json


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
                    if float(w.desire_price) >= float(product.current_price):
                        to_list.append(w.user.email)
                content = 'Type: ' + product.type + '\n'
                content += 'Item: ' + product.name + '\n'
                content += 'Sku: ' + product.uuid + '\n'
                content += 'Current Price: ' + str(product.current_price) + '\n'
                content += 'Reason: Price Drop\n'
                content += 'Item Link: ' + product.url + '\n'
                content += 'Amazon Link: ' \
                           + 'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=' \
                           + product.name
                send_mail(product.name + '\'s price been updated', content,
                          'brochuredev@126.com', to_list, fail_silently=False)
                print 'After:' + str(product.current_price)

    def query(self, url):
        p = {}
        r = requests.get(url, headers=self.headers)
        html = r.content
        price = re.findall(r'price">(?:\$|<span class="denominator">\$</span>)([\d.,]+)(</span>|</div>)', html, re.DOTALL)
        name = re.findall(r'<meta property="og:title" content="(.*?)"/>', html, re.DOTALL)

        p['current_price'] = price[0][0]
        p['uuid'] = self.get_uuid(url)
        product_query = ProductQuery.sku(int(p['uuid'])).show_all()
        api_url = product_query.url(self.api_key,  pid=int(self.get_pid(url)))
        r = requests.get(api_url, headers=self.headers)
        j = json.loads(r.content)

        p['name'] = j.get('name', None)
        p['type'] = j.get('type', None)
        p['original_price'] =  j.get('regularPrice', None)
        return p

    @staticmethod
    def get_uuid(url):
        sku = int(re.findall(r'skuId=(\d+)&', url)[0])
        return sku

    @staticmethod
    def get_pid(url):
        return re.findall(r'id=([\d]+)', url)[0]

    @staticmethod
    def get_type(html):
        return

if __name__ == '__main__':
    u = 'http://www.bestbuy.com/site/duke-nukem-forever-windows/2435079.p?id=1218328201673&skuId=2435079&strId=1436&strClr=true&ld=39.42216&lg=-76.78031&rd=25'
    b = BestBuySpider()
    print b.query(u)
