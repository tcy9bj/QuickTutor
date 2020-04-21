from django.test import TestCase, Client
from django.contrib.auth.models import User
from users.models import Profile
from users.forms import UserUpdateForm, ProfileUpdateForm

class UpdateFormsTestCase(TestCase):

    def test_UserUpdateForm_valid(self):
        '''Tests that the UserUpdateForm takes valid input'''
        user_form = UserUpdateForm(data={'username':"tester1", 'email':"tester1@gmail.com"})
        self.assertTrue(user_form.is_valid())

    def test_ProfileUpdateForm_valid(self):
        '''Tests that the ProfileUpdateForm takes valid input'''
        profile_form = ProfileUpdateForm(data={'first_name':'Joe', 'last_name':'Smith', 'major':'Spanish',
		                                       'major2':'Foreign Affairs', 'phone_number':'909-285-7438',
                                               'description':'This is a test profile.'})
        self.assertTrue(profile_form.is_valid())

    def test_UserUpdateForm_invalid(self):
        '''
        -Tests that the UserUpdateForm rejects invalid input
        -invalid test input: No email address
        '''
        user_form = UserUpdateForm(data={'username':"tester1", 'email':"John@gmail"})
        self.assertFalse(user_form.is_valid())

    def test_ProfileUpdateForm_invalid(self):
        '''
        -Tests that the ProfileUpdateForm rejects invalid input
        -invalid test input: Improper phone number format
        '''
        profile_form = ProfileUpdateForm(data={'first_name':'Joe', 'last_name':'Smith', 'major':'Spanish',
                                               'major2':'Foreign Affairs', 'phone_number':'9092857438',
                                               'description':'This is a test profile.'})
        self.assertFalse(profile_form.is_valid())

    def test_ProfileUpdateForm_valid_only_required_fields(self):
        '''Tests that the ProfileUpdateForm is still valid when non-required fields are left blank'''
        profile_form = ProfileUpdateForm(data={'first_name':'Joe', 'last_name':'Smith', 'major':'Spanish',
                                               'phone_number':'909-285-7438'})
        self.assertTrue(profile_form.is_valid())

class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", email="tester@gmail.com", first_name="John"
                                                                                   , last_name="Smith")
        self.client = Client()

    def test_profile_created_when_user_created(self):
        '''
        -A user profile is automatically created when a new user is created
        -Profile.image has default value: default.png
        -Profile.initialized has default value: False
        '''
        self.assertEqual(self.user.profile.image, "default.png")
        self.assertFalse(self.user.profile.initialized)

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
