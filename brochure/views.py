from django.shortcuts import render_to_response, HttpResponse
from spider.bestbuy import BestBuySpider
from spider.msstore import MSStoreSpider
from spider.radioshack import RadioShackSpider
from spider.staples import StaplesSpider
from spider.homedepot import HomeDepotSpider
import json
from django.views.decorators.csrf import csrf_exempt
from brochure.models import *
from django.core import serializers
from django.core import management


def home(request):
    return render_to_response('home.html', locals())

@csrf_exempt
def query(request):
    if request.method == 'POST':
        url = json.loads(request.body).get('url', None)
        store_name = json.loads(request.body).get('store_name', None)
        print store_name
        product = None
        if store_name == 'bestbuy':
            bb = BestBuySpider()
            product = bb.query(url)
        elif store_name == 'msstore':
            mss = MSStoreSpider()
            product = mss.query(url)
        elif store_name == 'radio':
            radio = RadioShackSpider()
            product = radio.query(url)
        elif store_name == 'staples':
            staple = StaplesSpider()
            product = staple.query(url)
        elif store_name == 'home':
            home = HomeDepotSpider()
            product = home.query(url)
        return HttpResponse(json.dumps(product), content_type="application/json")

@csrf_exempt
def get_items(request):
    store_name = json.loads(request.body).get('store_name', None)
    print store_name
    products = Product.objects.filter(website=store_name)
    return HttpResponse(serializers.serialize('json', products), content_type="application/json")

@csrf_exempt
def get_watchlist(request):
    store_name = json.loads(request.body).get('store_name', None)
    print store_name
    watchlist = Watchlist.objects.filter(product__website=store_name)
    return HttpResponse(serializers.serialize('json', watchlist), content_type="application/json")

@csrf_exempt
def add_item(request):
    if request.method == 'POST':
        store_name = json.loads(request.body).get('store_name', None)
        j = json.loads(request.body)
        url = j.get('url', None)
        name = j.get('name', None).decode('string-escape')
        # original_price = j.get('original_price', None).replace(',', '')
        sale_price = j.get('current_price', None).replace(',', '')
        desire_price = j.get('desire_price', None).replace(',', '')
        email = j.get('email', None)
        print desire_price, email
        p = Product(name=name, url=url, current_price=sale_price, original_price=0.0, error=False, website=store_name)
        p.save()
        w = Watchlist(email=email, product=p, desire_price=desire_price)
        w.save()
        return HttpResponse(json.dumps({'info': 0}), content_type="application/json")


def sync(request):
    management.call_command('runcrons')
    return HttpResponse(json.dumps({'info': 0}), content_type="application/json")