from django.conf.urls.defaults import *
from guestbook.views import IndexView, SignView

urlpatterns = patterns('',
	url(r'^$', IndexView.as_view(), name='index', ),
	url(r'^sign/$', SignView.as_view(), name='sign'),
)
