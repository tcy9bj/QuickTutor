from django.test import TestCase
from django.urls import reverse

'''
class TutorViewsTest(TestCase):
	def test_home(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
'''

class AdditionTest(TestCase):
	def test_add(self):
		self.assertEqual(1+1, 2)
