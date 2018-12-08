from django.conf.urls import url
from . import view
 
urlpatterns = [
    url('api/Login', view.Login),
    url('api/Score', view.Score),
    url('api/Notice', view.Notice),
    url('api/Table', view.Table),
    url('api/GPA', view.GPA),
]