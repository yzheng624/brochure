from spider_base import BaseSpider
import re
import requests
from brochure.models import *
from helper import send_mail


class HomeDepotSpider(BaseSpider):
    def __init__(self):
        BaseSpider.__init__(self)

    def run(self):
        print 'HomeDepot: run'
        products = Product.objects.filter(website='home')
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
                    user = w.user
                    s = Setting.objects.filter(user=user).get()
                    if float(w.desire_price) >= float(product.current_price):
                        if float(product.original_price) > float(s.amount):
                            if int(product.original_price) != 0:
                                if float(product.original_price) * float(s.percent) > float(product.current_price):
                                    to_list.append(w.email)
                            else:
                                to_list.append(w.email)
                send_mail(product, to_list)
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
