from spider_base import BaseSpider
import re
import requests


class RadioShackSpider(BaseSpider):
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
        price = re.findall(r'<span class="price">&#036;([\d.,]+)</span>', html, re.DOTALL)
        print price
        name = re.findall(r'<strong>(.*?)</strong>', html, re.DOTALL)
        p['name'] = name[0].split('"')[0]
        p['current_price'] = price[0]
        # p['original_price'] = price[1][0]
        return p

if __name__ == '__main__':
    u = 'http://www.radioshack.com/product/index.jsp?productId=13097267&znt_campaign=Category_CMS&znt_source=CAT&znt_medium=RSCOM&znt_content=CT2056569'
    m = RadioShackSpider()
    print m.query(u)
