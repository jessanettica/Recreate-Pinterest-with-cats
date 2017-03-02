from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_all_pins/$', views.get_all_pins, name='get-all-pins'),
    url(r'^get_more_pins/$', views.get_more_pins, name='get-more-pins'),
    url(r'^create_new_pin/$', views.create_new_pin, name='create-new-pin'),

]
