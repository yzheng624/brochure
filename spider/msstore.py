from spider_base import BaseSpider
import re
import requests
try:
    from brochure.models import *
except:
    pass
import HTMLParser
from helper import send_mail


class MSStoreSpider(BaseSpider):
    def __init__(self):
        BaseSpider.__init__(self)

    def run(self):
        print 'MSStore: run'
        products = Product.objects.filter(website='msstore')
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
        #try:
        price = re.findall(r'<meta name="twitter:data1" content="[\w]* ?\$([\d.,]+)"/>', html, re.DOTALL)
        if len(price) == 0:
            price = re.findall(r'<span itemprop="price">\$([\d.,]+) ?</span>', html)
        name = re.findall(r'<meta name="twitter:title" content="(.*?)"/>', html, re.DOTALL)
        if len(name) == 0:
            name = re.findall(r'pname: \[\'(.*?)\'\]', html, re.DOTALL)
        print name
        original = re.findall(r'strikethrough">\$([\d,.]+)</span>', html)
        h = HTMLParser.HTMLParser()
        p['name'] = h.unescape(name[0].split('"')[0])
        p['current_price'] = price[0].replace(',', '')
        p['uuid'] = self.get_uuid(url)
        try:
            p['original_price'] = original[0].replace(',', '')
        except:
            p['original_price'] = 0.0
        type = re.findall(r'busgrp : \[\'([\w]+)\'\]', html)
        p['type'] = type[0]
        #except:
        #    price = re.findall(r'<span itemprop="price">\$([\d.,]+) ?</span>', html)
        #    p = {
        #        'current_price': price[0],
        #        'uuid': self.get_uuid(url),
        #        'original_price':
        #    }
        return p

    def query_page(self, url):
        r = requests.get(url, headers=self.headers)
        html = r.content
        t = re.findall(r'<a href="([a-zA-Z0-9_\-\./]+?)" pid-ref="[\d]+" class="product-control">', html, re.DOTALL)
        for i in range(len(t)):
            t[i] = 'http://www.microsoftstore.com' + t[i]
        return t

    @staticmethod
    def get_uuid(url):
        return url.split('.')[-1]

if __name__ == '__main__':
    u = 'http://www.microsoftstore.com/store/msusa/en_US/pdp/Acer-Aspire-A5600U-UR11-Touchscreen-All-in-One/productID.275592200'
    u1 = 'http://www.microsoftstore.com/store/msusa/en_US/list/parentCategoryID.63436800/categoryID.63436900?'
    m = MSStoreSpider()
    # print m.query(u)
    print len(m.query_page(u1))
