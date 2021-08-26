from django.urls import path
from . import views

from django.conf.urls import url

urlpatterns = [
    url(r'^getfilename', views.get_filename, name='index'),
    url(r'^upload', views.upload_file, name='index'),
    url(r'^download', views.download_file, name='index'),
]