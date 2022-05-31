import imp
from django.forms import ModelForm
from client.models import UxClient, CreateTests


class ClientForm(ModelForm):
    class Meta:
        model = UxClient
        fields = '__all__'

class CreateTestForm(ModelForm):
    class Meta:
        model = CreateTests
        fields = '__all__'