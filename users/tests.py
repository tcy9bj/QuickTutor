from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Profile, Comment
from tutor.models import Ask
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
        self.user.profile.description = "This is a test profile."
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

    def test_register_view_not_accept_invalid_input(self):
        self.assertFalse(self.user.profile.initialized)
        post_data = {'user':self.user, 'username':'tester1', 'email':'tester1@gmail.com', 
                     'first_name':'Joe','last_name':'Smith', 'major':'Spanish', 'major2':'Foreign Affairs',
                     'phone_number':'9092857438', 'description':'This test succeeded'}
        response = self.client.post('/users/register/', post_data, follow=True)
        profile_id = self.user.profile.id
        profile = Profile.objects.get(id=profile_id)
        self.assertFalse(profile.initialized)

    def test_update_profile_view(self):
        profile_id = self.user.profile.id
        post_data = {'user':self.user, 'username':'tester1', 'email':'tester1@gmail.com', 
                     'first_name':'Joe','last_name':'Smith', 'major':'Spanish', 'major2':'Foreign Affairs',
                     'phone_number':'909-285-7438', 'description':'This test succeeded'}
        view_url = '/users/profile/'+str(profile_id)+'/edit/'
        response = self.client.post(view_url, post_data, follow=True)
        profile = Profile.objects.get(id=profile_id)
        self.assertEqual(profile.description, 'This test succeeded')

    def test_update_profile_view_not_accept_invalid_input(self):
        profile_id = self.user.profile.id
        post_data = {'user':self.user, 'username':'tester1', 'email':'tester1@gmail.com', 
                     'first_name':'','last_name':'Smith', 'major':'Spanish', 'major2':'Foreign Affairs',
                     'phone_number':'909-285-7438', 'description':'This test succeeded'}
        view_url = '/users/profile/'+str(profile_id)+'/edit/'
        response = self.client.post(view_url, post_data, follow=True)
        profile = Profile.objects.get(id=profile_id)
        self.assertEqual(profile.description, 'This is a test profile.')


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", email="tester@gmail.com", first_name="John"
                                                                                   , last_name="Smith")
        self.user.profile.description = "This is a test profile."
        self.client = Client()
        self.client.force_login(self.user)

    def test_profile_view(self):
        profile_id = self.user.profile.id
        response = self.client.get('/users/profile/'+str(profile_id)+'/')
        self.assertIn(response.status_code, [200, 302])

    def test_inbox_view(self):
        profile_id = self.user.profile.id
        response = self.client.get('/users/inbox/')
        self.assertIn(response.status_code, [200, 302])


class AskTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="tester1", email="tester1@gmail.com", first_name="John", last_name="Smith")
        self.user2 = User.objects.create(username="tester2", email="tester2@gmail.com", first_name="Jane", last_name="Doe")
        self.client = Client()
        self.client.force_login(self.user1)

        self.ask = Ask.objects.create(sender=self.user1, receiver=self.user2, course='CS 3240', question='How do I write tests?')

    def test_ask_detail_view(self):
        ask_id = self.ask.id
        response = self.client.get('/users/request/'+str(ask_id)+'/')
        self.assertIn(response.status_code, [200, 302])

    def test_AskDeleteView_valid_user(self):
        response = self.client.post(reverse('ask-delete', kwargs={'pk':self.ask.id}), follow=True)
        self.assertFalse(Ask.objects.filter(pk=self.ask.id).exists())

    def test_AskDeleteView_invalid_user(self):
        client2 = Client()
        client2.force_login(self.user2)
        response = client2.post(reverse('ask-delete', kwargs={'pk':self.ask.id}), follow=True)
        self.assertTrue(Ask.objects.filter(pk=self.ask.id).exists())

    def test_AskCompleteView_valid_user(self):
        self.user2.profile.current_client = self.ask
        client2 = Client()
        client2.force_login(self.user2)
        response = client2.post(reverse('ask-complete', kwargs={'pk':self.ask.id}), follow=True)
        self.assertFalse(Ask.objects.filter(pk=self.ask.id).exists())

    def test_AskCompleteView_invalid_user(self):
        response = self.client.post(reverse('ask-complete', kwargs={'pk':self.ask.id}), follow=True)
        self.assertTrue(Ask.objects.filter(pk=self.ask.id).exists())

    def test_accept_ask_view_marks_as_accepted(self):
        client2 = Client()
        client2.force_login(self.user2)
        response = client2.post(reverse('ask-accept', kwargs={'ask_id':self.ask.id}), follow=True)
        ask = Ask.objects.get(pk=self.ask.id)
        self.assertTrue(ask.accepted)

    def test_accept_ask_view_set_current_client(self):
        client2 = Client()
        client2.force_login(self.user2)
        response = client2.post(reverse('ask-accept', kwargs={'ask_id':self.ask.id}), follow=True)
        ask = Ask.objects.get(pk=self.ask.id)
        user2 = User.objects.get(pk=self.user2.id)
        self.assertEqual(ask, user2.profile.current_client)

    def test_accept_ask_view_rejects_if_already_current_client(self):
        ask2 = Ask.objects.create(sender=self.user1, receiver=self.user2, course='CS 2150', question="*Seinfeld voice* What's the deal with AVL trees?")
        self.user2.profile.current_client = ask2
        client2 = Client()
        client2.force_login(self.user2)
        response = client2.post(reverse('ask-accept', kwargs={'ask_id':self.ask.id}), follow=True)
        ask = Ask.objects.get(pk=self.ask.id)
        self.assertFalse(ask.accepted)

    def test_decline_ask_view_marks_as_declined(self):
        client2 = Client()
        client2.force_login(self.user2)
        response = client2.post(reverse('ask-decline', kwargs={'ask_id':self.ask.id}), follow=True)
        ask = Ask.objects.get(pk=self.ask.id)
        self.assertTrue(ask.declined)


class CommentTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="tester1", email="tester1@gmail.com", first_name="John", last_name="Smith")
        self.user2 = User.objects.create(username="tester2", email="tester2@gmail.com", first_name="Jane", last_name="Doe")
        self.client = Client()
        self.client.force_login(self.user1)

        self.comment = Comment.objects.create(reviewer=self.user1, reviewee=self.user2, rating=8, comment_text="A comment for testing.")

    def test_FeedbackForm_valid(self):
        form_data = {'rating':7, 'comment_text':"Test comment."}
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_FeedbackForm_invalid_1(self):
        form_data = {'rating':7, 'comment_text':''}
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_FeedbackForm_invalid_2(self):
        form_data = {'rating':'', 'comment_text':''}
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_FeedbackForm_invalid_3(self):
        form_data = {'rating':7.5, 'comment_text':'Test comment.'}
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_FeedbackForm_invalid_4(self):
        form_data = {'rating':-1, 'comment_text':'Test comment.'}
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_FeedbackForm_invalid_5(self):
        form_data = {'rating':11, 'comment_text':'Test comment.'}
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_CreatCommentView_creates_valid_comment(self):
        post_data = {'rating':7, 'comment_text':"This is a test comment."}
        response = self.client.post(reverse('review', kwargs={'pk':self.user2.id}), post_data, follow=True)
        self.assertTrue(Comment.objects.filter(comment_text="This is a test comment.").exists())

    def test_CreatCommentView_invalid_comment_1(self):
        post_data = {'rating':'', 'comment_text':"This is a test comment."}
        response = self.client.post(reverse('review', kwargs={'pk':self.user2.id}), post_data, follow=True)
        self.assertFalse(Comment.objects.filter(comment_text="This is a test comment.").exists())

    def test_CreatCommentView_invalid_comment_2(self):
        post_data = {'rating':7, 'comment_text':''}
        response = self.client.post(reverse('review', kwargs={'pk':self.user2.id}), post_data, follow=True)
        self.assertFalse(Comment.objects.filter(comment_text="This is a test comment.").exists())

    def test_CreatCommentView_no_data(self):
        post_data = {'rating':'', 'comment_text':''}
        response = self.client.post(reverse('review', kwargs={'pk':self.user2.id}), post_data, follow=True)
        self.assertFalse(Comment.objects.filter(comment_text="This is a test comment.").exists())

    def test_CreateCommentView_correctly_sets_tutor_score(self):
        self.user2.profile.tutor_score = 10
        self.user2.profile.num_ratings = 1
        self.user2.profile.save()

        post_data = {'rating':8, 'comment_text':"This is a test comment."}
        response = self.client.post(reverse('review', kwargs={'pk':self.user2.id}), post_data, follow=True)
        user2 = User.objects.get(pk=self.user2.id)
        self.assertEqual(user2.profile.tutor_score, 9)

    def test_DeleteCommentView_valid_user(self):
        self.user2.profile.tutor_score = 8
        self.user2.profile.num_ratings = 1
        self.user2.profile.save()

        response = self.client.post(reverse('comment-delete', kwargs={'user_id':self.user2.id, 'pk':self.comment.id}), follow=True)
        self.assertFalse(Comment.objects.filter(pk=self.comment.id).exists())

    def test_DeleteCommentView_invalid_user(self):
        self.user2.profile.tutor_score = 8
        self.user2.profile.num_ratings = 1
        self.user2.profile.save()
        client2 = Client()
        client2.force_login(self.user2)

        response = client2.post(reverse('comment-delete', kwargs={'user_id':self.user2.id, 'pk':self.comment.id}), follow=True)
        self.assertTrue(Comment.objects.filter(pk=self.comment.id).exists())

    def test_DeleteCommentView_correctly_sets_tutor_score(self):
        self.user2.profile.tutor_score = 9
        self.user2.profile.num_ratings = 2
        self.user2.profile.save()

        response = self.client.post(reverse('comment-delete', kwargs={'user_id':self.user2.id, 'pk':self.comment.id}), follow=True)
        user2 = User.objects.get(pk=self.user2.id)
        self.assertEqual(user2.profile.tutor_score, 10)
