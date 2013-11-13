from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'brochure.views.home'),
    url(r'^query/$', 'brochure.views.query'),
    url(r'^get_items/$', 'brochure.views.get_items'),
    url(r'^add_item/$', 'brochure.views.add_item'),
    url(r'^get_watchlist/$', 'brochure.views.get_watchlist'),
    url(r'^sync/$', 'brochure.views.sync'),
    url(r'^signin/$', 'brochure.views.signin'),
    url(r'^signup/$', 'brochure.views.signup'),
    url(r'^delete_items/$', 'brochure.views.delete_items'),
    url(r'^signout/$', 'brochure.views.signout'),
    url(r'^set_mark/$', 'brochure.views.set_mark'),
    url(r'^save_settings/$', 'brochure.views.save_settings'),
    url(r'^update_price/$', 'brochure.views.update_price'),
    url(r'^welcome.html$', 'brochure.views.welcome_html'),
    url(r'^product.html$', 'brochure.views.product_html'),
    url(r'^page.html$', 'brochure.views.page_html'),
    url(r'^add_product.html$', 'brochure.views.add_product_html'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
