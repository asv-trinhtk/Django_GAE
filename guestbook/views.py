from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView

from google.appengine.api import users

from guestbook.models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME

import logging
import urllib

def main_page(request):
    guestbook_name = request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)

    # Ancestor Queries, as shown here, are strongly consistent with the High
    # Replication Datastore. Queries that span entity groups are eventually
    # consistent. If we omitted the ancestor from this query there would be
    # a slight chance that Greeting that had just been written would not
    # show up in a query.
    greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
    greetings = greetings_query.fetch(10)

    # if users.get_current_user():
    #     url = users.create_logout_url(request.get_full_path())
    #     url_linktext = 'Logout'
    # else:
    #     url = users.create_login_url(request.get_full_path())
    #     url_linktext = 'Login'
    # url = users.create_login_url(request.get_full_path())
    url = ''
    url_linktext = 'Login'

    template_values = {
        'greetings': greetings,
        'guestbook_name': guestbook_name,
        'url': url,
        'url_linktext': url_linktext,
    }
    return render(request, 'guestbook/main_page.html', template_values)

def sign_post(request):
    if request.method == 'POST':
        guestbook_name = request.POST.get('guestbook_name')
        if guestbook_name is None or guestbook_name == '':
            guestbook_name = DEFAULT_GUESTBOOK_NAME

        greeting = Greeting(parent=guestbook_key(guestbook_name))

        # if users.get_current_user():
        #     greeting.author = users.get_current_user()

        greeting.content = request.POST.get('content')
        greeting.put()
        return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
    return HttpResponseRedirect('/')

class MainPage(ListView):
    template_name = 'guestbook/main_page.html'
    context_object_name = 'greetings'
    model = Greeting

    def get_guestbook_name(self):
        guestbook_name = self.request.GET.get('guestbook_name')
        if not guestbook_name or guestbook_name == '':
            guestbook_name = DEFAULT_GUESTBOOK_NAME
        return guestbook_name

    def get_queryset(self):
        guestbook_name = self.get_guestbook_name()
        return Greeting.query(ancestor=guestbook_key(guestbook_name)).order(
            -Greeting.date).fetch(5)

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        context['url_linktext'] = 'Login'
        context['guestbook_name'] = self.get_guestbook_name()
        return context

