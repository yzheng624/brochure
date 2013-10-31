from django.shortcuts import render_to_response

def home(request):
    return render_to_response('home.html', locals())

def bestbuy(request):
    return render_to_response('bestbuy.html', locals())

