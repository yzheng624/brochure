from django.shortcuts import render_to_response, HttpResponse
from spider.bestbuy import BestBuySpider
import json
from django.views.decorators.csrf import csrf_exempt
from brochure.models import *

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
    return HttpResponse(json.dumps(products), content_type="application/json")
