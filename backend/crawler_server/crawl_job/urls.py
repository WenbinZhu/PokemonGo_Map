from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'^$', views.add_crawl_point, name='add_crawl_point')
]
