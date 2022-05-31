import imp
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from .models import UxTester



class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        customer=UxTester.objects.get(user=user.pk)
        return six.text_type(user.pk)+six.text_type(timestamp)+ six.text_type(customer.is_email_verified)




generate_token =TokenGenerator()