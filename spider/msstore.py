from spider_base import BaseSpider
import re
import requests
from brochure.models import *
import HTMLParser


class MSStoreSpider(BaseSpider):
    def __init__(self):
        BaseSpider.__init__(self)

    def run(self):
        products = Product.objects.all()
        for product in products:
            print product.name
            print 'Before:' + str(product.current_price)
            p = self.query(product.url)
            if product.current_price != float(p['current_price']):
                product.current_price = p['current_price']
                product.save()
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
        p['current_price'] = price[0]
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

    @staticmethod
    def get_uuid(url):
        return url.split('.')[-1]

if __name__ == '__main__':
    u = 'http://www.microsoftstore.com/store/msusa/en_US/pdp/Acer-Aspire-A5600U-UR11-Touchscreen-All-in-One/productID.275592200'
    m = MSStoreSpider()
    print m.query(u)
