from django.conf.urls.defaults import *
from guestbook.views import MainPage, main_page, sign_post

urlpatterns = patterns('',
    url(r'^sign/$', sign_post),
    url(r'^$', MainPage.as_view(), name='index',),

)