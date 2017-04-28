from google.appengine.api import mail, taskqueue
import webapp2
import settings
import logging

def add_queue_send_mail(user, guestbook_name):
	if user:
		logging.info('Send mail guestbook')
		sender = user
		to = 'test@aoi-sys.vn'
		subject = 'Sign New Guestbook %s' %(guestbook_name)
		body = ''
		task = taskqueue.Task(url='/task/sendmail',
			params = {
				'sender': sender,
				'to': to,
				'subject': subject,
				'body': body
			},
			countdown=10
		)
		queue = taskqueue.Queue('default')
		queue.add(task)


class SendMailQueueHandle(webapp2.RequestHandler):

	def post(self):
		sender = self.request.get('sender', '')
		if sender == '':
			logging.warn('Sender is empty.')
			return
		to = self.request.get('to')
		subject = self.request.get('subject')
		body = self.request.get('body')
		mail.send_mail(sender=sender,
			to=to,
			subject=subject,
			body=body
		)
		return

app = webapp2.WSGIApplication(
	[
		('/task/sendmail', SendMailQueueHandle)
	],
	debug=settings.DEBUG)
