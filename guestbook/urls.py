from django.conf.urls.defaults import *
from guestbook.views import MainPage, main_page, sign_post

urlpatterns = patterns('',
    (r'^sign/$', sign_post),
    (r'^$', MainPage),
)