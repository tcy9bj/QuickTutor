from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Ask
from .forms import RequestForm

class ViewsTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.user1 = User.objects.create(username="tester1", email="tester1@gmail.com", first_name="John", last_name="Smith")
		self.user2 = User.objects.create(username="tester2", email="tester2@gmail.com", first_name="Jane", last_name="Doe")

	def test_login_view(self):
		response = self.client.get('/tutor/login/')
		self.assertEqual(response.status_code, 200)

	def test_request_view(self):
		response = self.client.get('/tutor/home/')
		self.assertEqual(response.status_code, 302)

	def test_request_valid(self):
		user_request = RequestForm(data={'sender':self.user1, 'receiver':self.user2, 'course': 'CS1110', 'question': 'help me'})
		self.assertTrue(user_request.is_valid())
