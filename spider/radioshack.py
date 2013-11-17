from spider_base import BaseSpider
import re
import requests
from helper import send_mail
from brochure.models import *


class RadioShackSpider(BaseSpider):
    def __init__(self):
        BaseSpider.__init__(self)

    def run(self):
        print 'Radio: run'
        products = Product.objects.filter(website='radio')
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
        # TODO Track Price
        price = re.findall(r'<span class="price">&#036;([\d.,]+)</span>', html, re.DOTALL)
        name = re.findall(r'<strong>(.*?)</strong>', html, re.DOTALL)
        p['name'] = name[0].split('"')[0]
        p['current_price'] = price[0]
        price = re.findall(r'class="reg_price">&#036;([\d.,]+)</', html, re.DOTALL)
        p['original_price'] = price[0]
        p['uuid'] = self.get_uuid(url)
        # p['original_price'] = price[1][0]
        return p

    def query_page(self, url):
        r = requests.get(url, headers=self.headers)
        html = r.content
        t = re.findall(r'<h2 class="productTitle"><a href="(.*?)">', html, re.DOTALL)
        for i in range(len(t)):
            t[i] = 'http://www.radioshack.com' + t[i]
        print t
        return t

    @staticmethod
    def get_uuid(url):
        return re.findall(r'productId=([\d]+)', url)[0]

if __name__ == '__main__':
    u = 'http://www.radioshack.com/product/index.jsp?productId=13097267&znt_campaign=Category_CMS&znt_source=CAT&znt_medium=RSCOM&znt_content=CT2056569'
    m = RadioShackSpider()
    print m.query(u)
