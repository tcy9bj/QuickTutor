from django.test import TestCase, Client
from django.contrib.auth.models import User
from users.models import Profile, Comment
from users.forms import UserUpdateForm, ProfileUpdateForm, FeedbackForm

class UpdateFormsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", email="tester@gmail.com",
                                        first_name="John", last_name="Smith")
        self.client = Client()
        self.client.force_login(self.user)

    def test_UserUpdateForm_valid(self):
        '''Tests that the UserUpdateForm takes valid input'''
        form_data = {'username':"tester1", 'email':"tester1@gmail.com"}
        user_form = UserUpdateForm(data=form_data)
        self.assertTrue(user_form.is_valid())

    def test_ProfileUpdateForm_valid(self):
        '''Tests that the ProfileUpdateForm takes valid input'''
        form_data = {'first_name':'Joe', 'last_name':'Smith', 'major':'Spanish', 'major2':'Foreign Affairs',
                     'courses':'SPAN 1060', 'phone_number':'909-285-7438', 'description':'This is a test profile.'}
        profile_form = ProfileUpdateForm(data=form_data)
        self.assertTrue(profile_form.is_valid())

    def test_UserUpdateForm_invalid(self):
        '''
        -Tests that the UserUpdateForm rejects invalid input
        -invalid test input: No email address
        '''
        form_data = {'username':"tester1", 'email':"John@gmail"}
        user_form = UserUpdateForm(data=form_data)
        self.assertFalse(user_form.is_valid())

    def test_ProfileUpdateForm_invalid(self):
        '''
        -Tests that the ProfileUpdateForm rejects invalid input
        -invalid test input: Improper phone number format
        '''
        form_data = {'first_name':'Joe', 'last_name':'Smith', 'major':'Spanish', 'major2':'Foreign Affairs',
                     'phone_number':'9092857438','description':'This is a test profile.'}
        profile_form = ProfileUpdateForm(data=form_data)
        self.assertFalse(profile_form.is_valid())

    def test_ProfileUpdateForm_valid_only_required_fields(self):
        '''Tests that the ProfileUpdateForm is still valid when non-required fields are left blank'''
        form_data = {'first_name':'Joe', 'last_name':'Smith', 'major':'Spanish',
                     'phone_number':'909-285-7438'}
        profile_form = ProfileUpdateForm(data=form_data)
        self.assertTrue(profile_form.is_valid())

    def test_update_user_profile(self):
        self.assertFalse(self.user.profile.initialized)
        form_data = {'first_name':'Joe','last_name':'Smith', 'major':'Spanish', 'major2':'Foreign Affairs',
                     'courses':'SPAN 1060', 'phone_number':'909-285-7438', 'description':'This test succeeded'}
        profile_form = ProfileUpdateForm(form_data, instance=self.user.profile)
        self.assertTrue(profile_form.is_valid())
        profile = profile_form.save(commit=False)
        profile.user = self.user
        profile.initialized = True
        profile.save()
        self.assertTrue(self.user.profile.initialized)
        self.assertEqual(self.user.profile.description, "This test succeeded")

    def test_update_user_info(self):
        form_data = {'username':"tester1", 'email':'tester1@gmail.com'}
        user_form = UserUpdateForm(form_data, instance=self.user)
        self.assertTrue(user_form.is_valid())
        user_form.save()
        self.assertEqual(self.user.username, "tester1")
        self.assertEqual(self.user.email, "tester1@gmail.com")


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", email="tester@gmail.com", first_name="John"
                                                                                   , last_name="Smith")
        self.client = Client()
        self.client.force_login(self.user)

    def test_profile_created_when_user_created(self):
        '''
        -A user profile is automatically created when a new user is created
        -Profile.image has default value: default.png
        -Profile.initialized has default value: False
        '''
        self.assertEqual(self.user.profile.image, "default.png")
        self.assertFalse(self.user.profile.initialized)

    def test_register_view_fills_out_new_user_profiles(self):
        self.assertFalse(self.user.profile.initialized)
        post_data = {'user':self.user, 'username':'tester1', 'email':'tester1@gmail.com',
                     'first_name':'Joe','last_name':'Smith', 'major':'Spanish', 'major2':'Foreign Affairs',
                     'phone_number':'909-285-7438', 'description':'This test succeeded'}
        response = self.client.post('/users/register/', post_data, follow=True)
        profile_id = self.user.profile.id
        profile = Profile.objects.get(id=profile_id)
        self.assertTrue(profile.initialized)
        self.assertEqual(profile.description, 'This test succeeded')

class ReviewTestCases(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(username='tester1', email='tester1@gmail.com', first_name='John', last_name='Smith')
        self.user2 = User.objects.create(username='tester2', email='tester2@gmail.com', first_name='Jane', last_name='Doe')
        self.client = Client()

    def test_review_valid(self):
        user_request = FeedbackForm(data={'reviewer':self.user1, 'reviewee':self.user2, 'rating': '10', 'comment_text': 'Very helpful!'})
        self.assertTrue(user_request.is_valid())

    def test_review_invalid(self):
        '''Test required fields'''
        user_request = FeedbackForm(data={'reviewer':self.user1, 'reviewee':self.user2, 'rating': '10', 'comment_text': ''})
        self.assertFalse(user_request.is_valid())

    def test_review_invalid2(self):
        user_request = FeedbackForm(data={'reviewer':self.user1, 'reviewee':self.user2, 'rating': '', 'comment_text': 'Very helpful!'})
        self.assertFalse(user_request.is_valid())

    def test_review_invalid3(self):
        user_request = FeedbackForm(data={'reviewer':self.user1, 'reviewee':self.user2, 'rating': '', 'comment_text': ''})
        self.assertFalse(user_request.is_valid())

    def test_review_invalid4(self):
        '''Test rating bounds'''
        user_request = FeedbackForm(data={'reviewer':self.user1, 'reviewee':self.user2, 'rating': '11', 'comment_text': 'Very helpful!'})
        self.assertFalse(user_request.is_valid())
