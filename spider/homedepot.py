from spider_base import BaseSpider
import re
import requests


class HomeDepotSpider(BaseSpider):
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
        price = re.findall(r'var CI_ItemPrice=\'([\d.,]+)\';', html, re.DOTALL)
        name = re.findall(r'var CI_ItemName=\'(.*?)\';', html, re.DOTALL)
        p['name'] = name[0]
        p['current_price'] = price[0]
        p['uuid'] = self.get_uuid(html)
        # p['original_price'] = price[1][0]
        return p

    @staticmethod
    def get_uuid(html):
        q = re.findall(r'Internet # ([\d]+)</h2>', html)
        return q[0]

if __name__ == '__main__':
    u = 'http://www.homedepot.com/p/EcoSmart-14-Watt-75W-BR30-Soft-White-2700K-LED-Flood-Light-Bulb-4-Pack-ECS-BR30-W27-120-4PK/204627118?N=arcdZ6'
    m = HomeDepotSpider()
    print m.query(u)
