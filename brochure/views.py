from django.shortcuts import render_to_response, HttpResponse
from spider.bestbuy import BestBuySpider
import json
from django.views.decorators.csrf import csrf_exempt
from brochure.models import *
from django.core import serializers

def home(request):
    return render_to_response('home.html', locals())

@csrf_exempt
def query_bestbuy(request):
    if request.method == 'POST':
        url = json.loads(request.body).get('url', None)
        bb = BestBuySpider()
        product = bb.query(url)
        return HttpResponse(json.dumps(product), content_type="application/json")

@csrf_exempt
def add_bestbuy(request):
    if request.method == 'POST':
        url = json.loads(request.body).get('url', None)
        bb = BestBuySpider()
        product = bb.query(url)
        return HttpResponse(json.dumps(product), content_type="application/json")

def get_bestbuy(request):
    products = Product.objects.filter(website="bestbuy")
    return HttpResponse(serializers.serialize('json', products), content_type="application/json")

def get_watchlist(request):
    watchlist = Watchlist.objects.filter(product__website="bestbuy")
    return HttpResponse(serializers.serialize('json', watchlist), content_type="application/json")

@csrf_exempt
def add_watchlist(request):
    if request.method == 'POST':
        j = json.loads(request.body)
        url = j.get('url', None)
        name = j.get('name', None)
        # original_price = j.get('original_price', None).replace(',', '')
        sale_price = j.get('current_price', None).replace(',', '')
        desire_price = j.get('desire_price', None).replace(',', '')
        email = j.get('email', None)
        print desire_price, email
        p = Product(name=name, url=url, current_price=sale_price, original_price=0.0, error=False, website='bestbuy')
        p.save()
        w = Watchlist(email=email, product=p, desire_price=desire_price)
        w.save()
        return HttpResponse(json.dumps({'info': 0}), content_type="application/json")