from spider_base import BaseSpider
import re
import requests

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
        r = self.bot.get(url, headers=self.headers)
        html = r.content
        f = open('s.html', 'w')
        f.write(html)
        price = re.findall(r'<span class="finalPrice">\$([\d.,]+).</span>', html, re.DOTALL)
        print price
        name = re.findall(r'<title>(.*?)</title>', html, re.DOTALL)
        p['name'] = name[0].split('|')[0]
        p['current_price'] = price[0]
        # p['original_price'] = price[1][0]
        return p

if __name__ == '__main__':
    u = 'http://www.staples.com/Toshiba-C855-S5350-156-Laptop/product_984635'
    m = StaplesSpider()
    print m.query(u)
