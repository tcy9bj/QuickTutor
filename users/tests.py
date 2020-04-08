from django.test import TestCase, Client
from django.contrib.auth.models import User
from users.models import Profile
from users.forms import UserUpdateForm, ProfileUpdateForm

class UsersFormsTestCase(TestCase):

	def test_UserUpdateForm_and_ProfileUpdateForm_valid(self):
		'''Tests that the UserUpdateForm and ProfileUpdateForm take valid input'''
		user_form = UserUpdateForm(data={'username':"tester1", 'email':"tester1@gmail.com"})
		profile_form = ProfileUpdateForm(data={'first_name':'Joe', 'last_name':'Smith', 'major':'Spanish',
    										   'major2':'Foreign Affairs', 'phone_number':'909-285-7438',
    										   'description':'This is a test profile.'})
		self.assertTrue(user_form.is_valid())

	def ProfileUpdateForm_valid(self):
		user_form = UserUpdateForm(data={'username':"tester1", 'email':"tester1@gmail.com"})
		profile_form = ProfileUpdateForm(data={'first_name':'Joe', 'last_name':'Smith', 'major':'Spanish',
									   'major2':'Foreign Affairs', 'phone_number':'909-285-7438',
									   'description':'This is a test profile.'})
		self.assertTrue(profile_form.is_valid())


	def test_UserUpdateForm_invalid(self):
		'''
		-Tests that the UserUpdateForm and ProfileUpdateForm reject invalid input
		-invalid test input: No email address, Improper phone number format
		'''
		user_form = UserUpdateForm(data={'username':"tester1", 'email':""})
		profile_form = ProfileUpdateForm(data={'first_name':'Joe', 'last_name':'Smith', 'major':'Spanish',
    										   'major2':'Foreign Affairs', 'phone_number':'9092857438',
    										   'description':'This is a test profile.'})
		self.assertFalse(user_form.is_valid())


	def ProfileUpdateForm_invalid(self):
		user_form = UserUpdateForm(data={'username':"tester1", 'email':""})
		profile_form = ProfileUpdateForm(data={'first_name':'Joe', 'last_name':'Smith', 'major':'Spanish',
    										   'major2':'Foreign Affairs', 'phone_number':'9092857438',
    										   'description':'This is a test profile.'})
		self.assertFalse(profile_form.is_valid())

	def UserForm_NoSecondMjr(self):
		user_form = UserUpdateForm(data={'username':"tester1", 'email':""})
		profile_form = ProfileUpdateForm(data={'first_name':'Joe', 'last_name':'Smith', 'major':'Spanish',
    										   'phone_number':'9092857438', 'description':'This is a test profile.'})
		self.assertTrue(user_form.is_valid())


class ProfileTestCase(TestCase):
    def setUp(self):
    	self.user = User.objects.create(username="tester", email="tester@gmail.com", first_name="John"
    																			   , last_name="Smith")
    	self.client = Client()


    def test_profile_created_when_user_created(self):
    	'''
    	-A user profile is automatically created when a new user is created
		-Profile.image has default value: default.png
    	'''
    	self.assertEqual(self.user.profile.image, "default.png")

    def test_name(self):

        self.assertEqual(self.user.first_name, 'John')

    def test_email(self):
        self.assertEqual(self.user.email, 'tester@gmail.com')

    def test_lName(self):
        self.assertTrue(self.user.last_name == 'Smith')

'''
    def test_register_view_fills_out_new_user_profiles(self):
    	self.client.force_login(self.user)
    	self.assertFalse(self.user.profile.initialized)
    	response = self.client.post('/users/register/', {'user':self.user, 'username':"tester1",
    										   'email':"tester1@gmail.com", 'first_name':'Joe',
    										   'last_name':'Smith', 'major':'Spanish',
    										   'major2':'Foreign Affairs', 'phone_number':'909-285-7438',
    										   'description':'This test succeeded'}, follow=True)
    	#self.assertEqual(response.redirect_chain, "")
    	self.assertTrue(self.user.profile.initialized)
    	self.assertEqual(self.user.profile.description, "This test succeeded")
'''
