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
from django.shortcuts import redirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


def home(request):
    if request.user.is_authenticated():
        if not Setting.objects.filter(user=request.user).exists():
            s = Setting(user=request.user)
            s.save()
        s = Setting.objects.filter(user=request.user).get()
        return render_to_response('home.html', locals())
    else:
        return redirect('/signin/')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            c = {}
            c.update(csrf(request))
            c['info'] = 'The username and password were incorrect.'
            return render_to_response('signin.html', c)
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('signin.html', c)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        user.save()
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('signup.html', c)

def signout(request):
    logout(request)
    return redirect('/')

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
        info = ''
        if Product.objects.filter(uuid=product['uuid'], website=store_name).exists():
            if Watchlist.objects.filter(user=request.user, product=Product.objects.filter(uuid=product['uuid'], website=store_name).get()).exists():
                info = 'Item has already been added.'
        product['info'] = info
        return HttpResponse(json.dumps(product), content_type="application/json")

@csrf_exempt
def get_items(request):
    store_name = json.loads(request.body).get('store_name', None)
    products = Product.objects.filter(website=store_name, watchlist__user=request.user).all()
    return HttpResponse(serializers.serialize('json', products), content_type="application/json")

@csrf_exempt
def get_watchlist(request):
    store_name = json.loads(request.body).get('store_name', None)
    watchlist = Watchlist.objects.filter(product__website=store_name, user=request.user)
    return HttpResponse(serializers.serialize('json', watchlist), content_type="application/json")

@csrf_exempt
def get_pages(request):
    store_name = json.loads(request.body).get('store_name', None)
    pages = Page.objects.filter(user=request.user, store_name=store_name)
    return HttpResponse(serializers.serialize('json', pages), content_type="application/json")

@csrf_exempt
def get_page_products(request):
    pk = json.loads(request.body).get('pk', None)
    page = Page.objects.filter(pk=pk).get()
    products = page.product.all()
    return HttpResponse(serializers.serialize('json', products), content_type="application/json")

@csrf_exempt
def add_item(request):
    if request.method == 'POST':
        j = json.loads(request.body)
        store_name = j.get('store_name', None)
        url = j.get('url', None)
        name = j.get('name', None)
        sale_price = str(j.get('current_price', None)).replace(',', '')
        desire_price = j.get('desire_price', None).replace(',', '')
        uuid = j.get('uuid', None)
        original_price = j.get('original_price', 0.0)
        email = j.get('email', None)
        p = Product(name=name, url=url, current_price=sale_price, original_price=original_price,
                    error=False, website=store_name, uuid=uuid, type=type, json={})
        p.save()
        w = Watchlist(user=request.user, product=p, desire_price=desire_price, email=email)
        w.save()
        return HttpResponse(json.dumps({'info': 0}), content_type="application/json")

@csrf_exempt
def add_page(request):
    if request.method == 'POST':
        j = json.loads(request.body)
        url = j.get('url', None)
        description = j.get('description', None)
        least_price = j.get('least_price', None)
        discount = j.get('discount', None)
        email = j.get('email', None)
        store_name = j.get('store_name', None)
        page = Page(url=url, description=description, error=False, user=request.user, least_price=least_price,
                    discount=discount, email=email, store_name=store_name)
        page.save()
        url_list = []
        spider = None
        if store_name == 'bestbuy':
            spider = BestBuySpider()
            url_list = spider.query_page(url)
        elif store_name == 'msstore':
            spider = MSStoreSpider()
            url_list = spider.query_page(url)
        elif store_name == 'radio':
            radio = RadioShackSpider()
            product = radio.query(url)
        elif store_name == 'staples':
            staple = StaplesSpider()
            product = staple.query(url)
        elif store_name == 'home':
            home = HomeDepotSpider()
            product = home.query(url)
        for url in url_list:
            try:
                product = spider.query(url)
            except:
                continue
            p = Product(name=product['name'], url=url, current_price=product['current_price'], original_price=product['original_price'],
                        error=False, website=store_name, uuid=product['uuid'], type=product['type'], json={})
            p.save()
            page.product.add(p)
            page.save()
        return HttpResponse(json.dumps({'info': 0}), content_type="application/json")

@csrf_exempt
def delete_items(request):
    if request.method == 'POST':
        dic = json.loads(request.body)
        for key in dic:
            if dic[key] == True:
                w = Watchlist.objects.filter(product__pk=key)
                w.delete()
    return HttpResponse(json.dumps({'info': 0}), content_type="application/json")

@csrf_exempt
def set_mark(request):
    if request.method == 'POST':
        j = json.loads(request.body)
        pk = j.get('pk', None)
        w = Watchlist.objects.filter(user=request.user, product__pk=pk).get()
        w.mark = (w.mark == False)
        w.save()
    return HttpResponse(json.dumps({'info': 0}), content_type="application/json")

@csrf_exempt
def save_settings(request):
    if request.method == 'POST':
        request.user.email = request.POST['email']
        request.user.save()
        s = Setting.objects.filter(user=request.user).get()
        s.per_product = request.POST['per_product']
        s.per_round = request.POST['per_round']
        s.amount = request.POST['amount']
        s.percent = request.POST['percent']
        s.save()
        return redirect('/')

@csrf_exempt
def update_price(request):
    if request.method == 'POST':
        j = json.loads(request.body)
        pk = j.get('pk', None)
        desire_price = j.get('desire_price', None)
        w = Watchlist.objects.filter(user=request.user, product__pk=pk).get()
        w.desire_price = desire_price
        w.save()
        return HttpResponse(json.dumps({'info': 0}), content_type="application/json")

def sync(request):
    management.call_command('runcrons')
    return HttpResponse(json.dumps({'info': 0}), content_type="application/json")


def product_html(reqest):
    return render_to_response('product.html')


def welcome_html(request):
    return render_to_response('welcome.html')


def page_html(request):
    return render_to_response('page.html')


def add_product_html(request):
    return render_to_response('add_product.html')


def add_page_html(request):
    return render_to_response('add_page.html')

def page_products_html(request):
    return render_to_response('page_products.html')