from django.contrib.auth.models import User
from django.test import TestCase

from password_policies.models import PasswordProfile, password_change_signal


class TestSignals(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="foo")

    def test_password_change_signal(self):
        self.user.password = "changed"
        PasswordProfile.objects.all().delete()
        assert password_change_signal(sender=None, instance=self.user) is None

    def test_password_created_signal(self):
        PasswordProfile.objects.get(user=self.user)
