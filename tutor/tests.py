from django.test import TestCase, Client
from django.urls import reverse

class ViewsTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_login_view(self):
		response = self.client.get('/tutor/login/')
		self.assertEqual(response.status_code, 200)
