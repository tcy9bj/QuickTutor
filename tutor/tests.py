from django.test import TestCase, Client
from django.urls import reverse

from .models import Ask
from .forms import RequestForm

class ViewsTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_login_view(self):
		response = self.client.get('/tutor/login/')
		self.assertEqual(response.status_code, 200)

	def test_request_view(self):
		response = self.client.get('/tutor/home/')
		self.assertEqual(response.status_code, 302)

	def test_request_valid(self):
		user_request = RequestForm(data={'fName': 'John', 'lName': 'Smith', 'subject': 'CS1110', 'question': 'help me'})
		self.assertTrue(user_request.is_valid())
