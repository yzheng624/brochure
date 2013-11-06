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

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
