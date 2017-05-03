from google.appengine.api import mail
from google.appengine.ext import ndb, deferred
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
import webapp2
import settings
import logging


def add_queue_send_mail(user, guestbook_name, text_content):
	if user:
		logging.info('Send mail guestbook')
		sender = user
		to = 'test@aoi-sys.vn'
		subject = 'Sign New Guestbook %s' % guestbook_name
		enqueue_task(send_mail_using_django, sender, to, subject, guestbook_name, text_content,
			_queue='email', _countdown=10, _transactional=True)


class SendMailQueueHandle(webapp2.RequestHandler):

	def post(self):
		sender = self.request.get('sender', '')
		if sender == '':
			logging.warn('Sender is empty.')
			return
		to = self.request.get('to')
		subject = self.request.get('subject')
		guestbook_name = self.request.get('guestbook_name')
		text_content = self.request.get('text_content')
		send_mail(sender, to, subject, guestbook_name, text_content)


def send_mail(sender, to, subject, guestbook_name, text_content):
	logging.info('start send_mail')
	mail.send_mail(sender=sender,
		to=to,
		subject=subject,
		body=text_content
	)
	return


def send_mail_using_django(sender, to, subject, guestbook_name, text_content):
	logging.info('send_mail_using_django')
	connect = get_connection()
	try:
		connect.open()
		html_content = render_to_string('guestbook/mail_content.html', {'user': sender,
		'guestbook_name': guestbook_name, 'content': text_content})
		msg = EmailMultiAlternatives(subject, text_content, sender, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
	except BaseException, e:
		raise e
	finally:
		connect.close()
	return


@ndb.transactional
def enqueue_task(func, *args, **kwargs):
	try:
		## using deferred
		deferred.defer(func, *args, **kwargs)
	except Exception, e:
		logging.error(e.__class__.__name__)
		raise


app = webapp2.WSGIApplication(
	[
		('/task/sendmail', SendMailQueueHandle)
	],
	debug=settings.DEBUG)
