from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from pins import views as pinviews

urlpatterns = [
    url(r'^$', 'pins.views.index', name='home'),
    url(r'^pins/', include('pins.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', pinviews.logout_page, name='logout'),
    url(r'^register/$', pinviews.register_page, name='register'),
    url(r'^admin/', include(admin.site.urls)),
]
