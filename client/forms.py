import imp
from django.forms import ModelForm
from client.models import UxClient


class ClientForm(ModelForm):
    class Meta:
        model = UxClient
        fields = '__all__'