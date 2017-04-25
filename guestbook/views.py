from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, ListView
from django.core.urlresolvers import reverse_lazy

from google.appengine.api import users

from guestbook.models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME
from guestbook.forms import SignForm
import logging

class IndexView(TemplateView):
    template_name = 'guestbook/main_page.html'
    context_object_name = 'greetings'

    def get_guestbook_name(self):
        guestbook_name = self.request.GET.get('guestbook_name')
        if not guestbook_name or guestbook_name == '':
            guestbook_name = DEFAULT_GUESTBOOK_NAME
        return guestbook_name

    def get_context_data(self, **kwargs):
        guestbook_name = self.get_guestbook_name()
        context = super(IndexView, self).get_context_data(**kwargs)
        context['guestbook_list'] = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date).fetch(5)
        context['url_linktext'] = 'Login'
        context['guestbook_name'] = guestbook_name

        return context

    def get(self, request, *args, **kwargs):
        sign_view = SignForm(self.request.GET or None)
        context = self.get_context_data(**kwargs)
        context['sign_form'] = sign_view

        return self.render_to_response(context)

class SignView(FormView):
    # template_name = 'guestbook/sign_page.html'
    template_name = 'guestbook/index.html'
    form_class = SignForm
    success_url = reverse_lazy('index')

    def sign_book(self, guestbook_name, content):
        if guestbook_name != '':
            greeting = Greeting(parent=guestbook_key(guestbook_name))
            greeting.content = content
            greeting.put()

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context['sign_form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, **kwargs):
        logging.info('form_valid')
        logging.info(form.cleaned_data['name'])
        self.sign_book(form.cleaned_data['name'], form.cleaned_data['content'])
        return super(SignView, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        # context = self.get_context_data(**kwargs)
        # context['form'] = form
        return render(self.request, 'guestbook/sign_error.html')

    def get_success_url(self, **kwargs):
        return reverse_lazy('index', kwargs={'guestbook_name': 'new'})

