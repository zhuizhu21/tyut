from django.conf.urls import url
from . import view
 
urlpatterns = [
    url('api2/Login', view.Login),
    url('appi2/Score', view.Score),
    url('api2/Notice', view.Notice),
    url('api2/Table', view.Table),
    url('api2/GPA', view.GPA),
]