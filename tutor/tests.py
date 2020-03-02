from django.test import TestCase
from django.urls import reverse

class AdditionTest(TestCase):
	def test_add(self):
		self.assertEqual(1+1, 2)
