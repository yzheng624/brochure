from spider_base import BaseSpider
import re
import requests
try:
    from brochure.models import *
except:
    pass
from premix import ProductQuery
import json
from helper import send_mail


class BestBuySpider(BaseSpider):
    def __init__(self):
        BaseSpider.__init__(self)
        self.api_key = '5q7nvwnwfm5bc9xk7qbgb3gb'

    def run(self):
        print 'BestBuy: run'
        products = Product.objects.filter(website='bestbuy')
        for product in products:
            print product.name
            print 'Before:' + str(product.current_price)
            try:
                p = self.query(product.url)
            except:
                p.error = True
            if str(product.current_price) != str(p['current_price']):
                prev_price = product.current_price
                product.current_price = float(p['current_price'])
                product.save()
                watchlist = Watchlist.objects.filter(product__pk=product.pk)
                to_list = []
                for w in watchlist:
                    user = w.user
                    s = Setting.objects.filter(user=user).get()
                    if float(w.desire_price) >= float(product.current_price):
                        if float(product.original_price) > float(s.amount):
                            if int(product.original_price) != 0:
                                if float(product.original_price) * float(s.percent) > float(product.current_price):
                                    to_list.extend(w.email.split(';'))
                            else:
                                to_list.extend(w.email.split(';'))
                send_mail(product, to_list)
                print 'After:' + str(product.current_price)

    def query(self, url):
        p = {}
        r = requests.get(url, headers=self.headers)
        html = r.content
        try:
            price = re.findall(r'price">(?:\$|<span class="denominator">\$</span>)([\d.,]+)(?:</span>|</div>)', html, re.DOTALL)
            print price
            product_query = ProductQuery.sku(self.get_uuid(url)).show_all()
            api_url = product_query.url(self.api_key,  pid=int(self.get_pid(url)))
            print api_url, 0
            r = requests.get(api_url, headers=self.headers)
            j = json.loads(r.content)
            p = {
                'name': j.get('name', None),
                'type': j.get('type', None),
                'current_price': price[0].replace(',', ''),
                'original_price': price[1].replace(',', ''),
                'uuid':  j.get('sku', None),
            }
        except:
            product_query = ProductQuery.sku(self.get_uuid(url)).show_all()
            api_url = product_query.url(self.api_key,  pid=int(self.get_pid(url)))
            print api_url, 1
            r = requests.get(api_url, headers=self.headers)
            j = json.loads(r.content)
            p = {
                'name': j.get('name', None),
                'type': j.get('type', None),
                'current_price': j.get('salePrice', None),
                'original_price': j.get('regularPrice', None),
                'uuid':  j.get('sku', None),
            }
        return p

    def query_page(self, url):
        print url
        r = requests.get(url, headers=self.headers)
        html = r.content
        t = re.findall(r'<a rel="product" href="(.+?)">', html, re.DOTALL)
        for i in range(len(t)):
            t[i] = 'http://www.bestbuy.com' + t[i]
        if len(t) > 0:
            q = url.split('=')
            url_raw = ''
            for p in q[:-1]:
                url_raw += p + '='
            t.extend(self.query_page(url_raw + str(int(q[-1]) + 1)))
        return t

    @staticmethod
    def get_uuid(url):
        sku = int(re.findall(r'skuId=(\d+)&?', url)[0])
        return sku

    @staticmethod
    def get_pid(url):
        return re.findall(r'id=([\d]+)', url)[0]

    @staticmethod
    def get_type(html):
        return

if __name__ == '__main__':
    u = 'http://www.bestbuy.com/site/duke-nukem-forever-windows/2435079.p?id=1218328201673&skuId=2435079&strId=1436&strClr=true&ld=39.42216&lg=-76.78031&rd=25'
    u2 = 'http://www.bestbuy.com/site/olstemplatemapper.jsp?_dyncharset=ISO-8859-1&id=pcat17080&type=page&lcn=Computers+%26+Tablets&sc=abComputerSP&usc=abcat0500000&cp=1&sp=-displaydate+skuid&nrp=15&qp=crootcategoryid~~cabcat0500000~~nf396||436c656172616e63652026204d6f7265'
    u3 = 'http://www.bestbuy.com/site/dell-xps-ultrabook-convertible-12-5-34-touch-screen-laptop-4gb-memory-carbon-fiber/7617041.p;jsessionid=50E46AE8D61064BE77B8BC718DEEDEDF.bbolsp-app04-177?id=1218855011514&skuId=7617041&strId=1516&strClr=true&ld=30.11261&lg=-97.35312&rd=25'
    b = BestBuySpider()
    print b.query(u3)
    # print b.query_page(u2)
