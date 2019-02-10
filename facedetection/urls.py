from django.conf.urls import url
# for face
from .views import tryit
urlpatterns=[
    url(r'^detection',tryit,name='tryit'),
]