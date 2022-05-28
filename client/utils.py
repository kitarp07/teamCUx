# generate one time token for security in emailverification

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import UxClient
import six

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp) :
        customer = UxClient.objects.get(user=user.pk)
        return six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(customer.isEmailVerified)
generate_token = TokenGenerator()