from django.test import TestCase
from django.contrib.auth.models import User
from tweet.models import Tweet

class UserSapIdTestCase(TestCase):
    def test_list_users_with_sap_id(self):
        # List all users with their sap_id
        for user in User.objects.all():
            print(f"Username: {user.username}, Email: {user.email}, SAP ID: {user.sap_id}")

    def test_list_tweets_with_sap_id(self):
        # List all tweets with their sap_id
        for tweet in Tweet.objects.all():
            print(f"Username: {tweet.user.username}, SAP ID: {tweet.sap_id}")
