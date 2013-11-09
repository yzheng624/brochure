from spider_base import BaseSpider
import re
import requests
from brochure.models import *
from helper import send_mail


class StaplesSpider(BaseSpider):
    def __init__(self):
        BaseSpider.__init__(self)
        self.bot = requests.session()
        data = {
            'zipCode': 21218,
            'storeId': 10001,
            'langId': -1,
            'URL': 'StaplesCategoryDisplay?catalogIdentifier=2&langId=-1&identifier=CL141985&storeId=10001',
            'errorUrl': 'zipcode'
        }
        self.bot.post('http://www.staples.com/office/supplies/StaplesZipCodeAdd?', data, headers=self.headers)

    def run(self):
        print 'Staples: run'
        products = Product.objects.filter(website='staples')
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
        r = self.bot.get(url, headers=self.headers)
        html = r.content
        price = re.findall(r'class="finalPrice">.*?\$([\d.,]+)', html, re.DOTALL)
        print price
        name = re.findall(r'<title>(.*?)</title>', html, re.DOTALL)
        p['name'] = name[0].split('|')[0]
        p['current_price'] = price[0]
        p['uuid'] = self.get_uuid(url)
        # p['original_price'] = price[1][0]
        return p

    @staticmethod
    def get_uuid(url):
        return url.split('_')[-1]

if __name__ == '__main__':
    u = 'http://www.staples.com/Toshiba-C855-S5350-156-Laptop/product_984635'
    m = StaplesSpider()
    print m.query(u)
