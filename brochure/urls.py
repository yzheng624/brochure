from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'brochure.views.home'),
    url(r'^query_bestbuy/$', 'brochure.views.query_bestbuy'),
    url(r'^add_bestbuy/$', 'brochure.views.add_bestbuy'),
    url(r'^get_bestbuy/$', 'brochure.views.get_bestbuy'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
