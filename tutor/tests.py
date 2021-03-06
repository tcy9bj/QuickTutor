from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from tutor.models import Ask
from users.models import Profile
from .forms import RequestForm

class ViewsTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.user1 = User.objects.create(username="tester1", email="tester1@gmail.com", first_name="John", last_name="Smith")
		self.user2 = User.objects.create(username="tester2", email="tester2@gmail.com", first_name="Jane", last_name="Doe")

	def test_login_view(self):
		response = self.client.get('/tutor/login/')
		self.assertEqual(response.status_code, 200)

	def test_home_view(self):
		response = self.client.get('/tutor/home/')
		self.assertIn(response.status_code, [200, 302])

	def test_request_view(self):
		tutor_id = self.user1.id
		response = self.client.get('/users/request/' + str(tutor_id) + '/')
		self.assertIn(response.status_code, [200, 302])

	def test_review_view(self):
		tutor_id = self.user1.id
		response = self.client.get('/users/profile/' + str(tutor_id) + '/review/')
		self.assertEqual(response.status_code, 302)

	def test_profile_view(self):
		tutor_id = self.user1.id
		response = self.client.get('/users/profile/' + str(tutor_id) + '/')
		self.assertIn(response.status_code, [200, 302])

	def test_FAQ_view(self):
		response = self.client.get('/tutor/FAQ/')
		self.assertEqual(response.status_code, 302)

	def test_logout_view(self):
		response = self.client.get('/tutor/accounts/logout/')
		self.assertEqual(response.status_code, 302)


class RequestsTest(TestCase):
	def setUp(self):
		self.user1 = User.objects.create(username="tester1", email="tester1@gmail.com", first_name="John", last_name="Smith")
		self.user2 = User.objects.create(username="tester2", email="tester2@gmail.com", first_name="Jane", last_name="Doe")
		self.client = Client()
		self.client.force_login(self.user1)

	def test_request_valid(self):
		form_data = {'sender':self.user1, 'receiver':self.user2, 'course': 'CS1110', 'question': 'What is an immutable type?'}
		user_request = RequestForm(data=form_data)
		self.assertTrue(user_request.is_valid())

	def test_request_invalid(self):
		form_data = {'sender':self.user1, 'receiver':self.user2, 'course': 'CS1110', 'question': ''}
		user_request = RequestForm(data=form_data)
		self.assertFalse(user_request.is_valid())

	def test_request_invalid2(self):
		user_request = RequestForm(data={'sender':self.user1, 'receiver':self.user2, 'course': '', 'question': 'Help please'})
		self.assertFalse(user_request.is_valid())

	def test_request_invalid3(self):
		user_request = RequestForm(data={'sender':self.user1, 'receiver':self.user2, 'course': '', 'question': ''})
		self.assertFalse(user_request.is_valid())

	def test_request_view_creates_Ask(self):
		user2_id = self.user2.id
		asks = self.user2.receiving_user.all()
		self.assertEqual(asks.count(), 0)
		post_data = {'user':self.user1, 'course':'CS 3240', 'question':'How do I write tests?'}
		view_url = '/tutor/request/'+str(user2_id)+'/'
		response = self.client.post(view_url, post_data, follow=True)
		asks_post = self.user2.receiving_user.all()
		self.assertEqual(asks_post.count(), 1)

	def test_request_view_invalid_input_1(self):
		user2_id = self.user2.id
		asks = self.user2.receiving_user.all()
		self.assertEqual(asks.count(), 0)
		post_data = {'user':self.user1, 'course':'', 'question':'How do I write tests?'}
		view_url = '/tutor/request/'+str(user2_id)+'/'
		response = self.client.post(view_url, post_data, follow=True)
		asks_post = self.user2.receiving_user.all()
		self.assertEqual(asks_post.count(), 0)

	def test_request_view_invalid_input_2(self):
		user2_id = self.user2.id
		asks = self.user2.receiving_user.all()
		self.assertEqual(asks.count(), 0)
		post_data = {'user':self.user1, 'course':'CS 3240', 'question':''}
		view_url = '/tutor/request/'+str(user2_id)+'/'
		response = self.client.post(view_url, post_data, follow=True)
		asks_post = self.user2.receiving_user.all()
		self.assertEqual(asks_post.count(), 0)

	def test_request_view_no_input(self):
		user2_id = self.user2.id
		asks = self.user2.receiving_user.all()
		self.assertEqual(asks.count(), 0)
		post_data = {'user':self.user1, 'course':'', 'question':''}
		view_url = '/tutor/request/'+str(user2_id)+'/'
		response = self.client.post(view_url, post_data, follow=True)
		asks_post = self.user2.receiving_user.all()
		self.assertEqual(asks_post.count(), 0)

	def test_requestRender_response(self):
		user2_id = self.user2.id
		asks = self.user2.receiving_user.all()
		self.assertEqual(asks.count(), 0)
		post_data = {'user':self.user1, 'course':'', 'question':''}
		view_url = '/tutor/request/'+str(user2_id)+'/'
		response = self.client.post(view_url, post_data, follow=True)
		asks_post = self.user2.receiving_user.all()
		self.assertTemplateUsed(response, 'tutor/request.html')

class ActiveTutorTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create(username="tester1", email="tester1@gmail.com", first_name="John", last_name="Smith")
		self.client.force_login(self.user)
		self.user.profile.first_name = "Joe"
		self.user.profile.last_name = "Smith"
		self.user.profile.major = "Spanish"
		self.user.profile.phone_number = "909-285-7438"
		self.user.profile.description = "This is a test profile."

	def test_activate_as_tutor(self):
		self.assertFalse(self.user.profile.active)
		post_data = {'location_selector': 'Alderman Library'}
		post_url = '/tutor/activate/' + str(self.user.id) + '/'
		response = self.client.post(post_url, post_data, follow=True)
		profile_id = self.user.profile.id
		profile = Profile.objects.get(id=profile_id)
		self.assertTrue(profile.active)
		self.assertEqual(profile.location, 'Alderman Library')

	def test_noLocation_activate(self):
		self.assertFalse(self.user.profile.active)
		post_url = '/tutor/activate/' + str(self.user.id) + '/'
		response = self.client.post(post_url, follow=True)
		profile_id = self.user.profile.id
		profile = Profile.objects.get(id=profile_id)
		self.assertFalse(profile.active)

	def test_deactivate_as_tutor(self):
		self.user.profile.active = True
		self.user.save()
		self.assertTrue(self.user.profile.active)
		post_url = '/tutor/deactivate/' + str(self.user.id) + '/'
		response = self.client.post(post_url, {}, follow=True)
		profile_id = self.user.profile.id
		profile = Profile.objects.get(id=profile_id)
		self.assertFalse(profile.active)

	def test_activeRender_response(self):
		self.user.profile.active = True
		self.user.save()
		self.assertTrue(self.user.profile.active)
		post_url = '/tutor/deactivate/' + str(self.user.id) + '/'
		response = self.client.post(post_url, {}, follow=True)
		profile_id = self.user.profile.id
		profile = Profile.objects.get(id=profile_id)
		self.assertTemplateUsed(response, 'tutor/home.html')
