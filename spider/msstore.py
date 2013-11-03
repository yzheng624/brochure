from spider_base import BaseSpider
import re
import requests


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
        price = re.findall(r'<meta name="twitter:data1" content="\$([\d.,]+)"/>', html, re.DOTALL)
        print price
        name = re.findall(r'<meta name="twitter:title" content="(.*?)"/>', html, re.DOTALL)
        p['name'] = name[0].split('"')[0]
        p['current_price'] = price[0]
        p['uuid'] = self.get_uuid(url)
        # p['original_price'] = price[1][0]
        return p

    @staticmethod
    def get_uuid(url):
        return url.split('.')[-1]

if __name__ == '__main__':
    u = 'http://www.microsoftstore.com/store/msusa/en_US/pdp/Acer-Aspire-A5600U-UR11-Touchscreen-All-in-One/productID.275592200'
    m = MSStoreSpider()
    print m.query(u)
