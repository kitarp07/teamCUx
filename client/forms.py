from dataclasses import field
import imp
from django.forms import ModelForm
from client.models import UxClient, CreateTests
from Tester.models import FeedBack

class ClientForm(ModelForm):
    class Meta:
        model = UxClient
        fields = '__all__'

class CreateTestForm(ModelForm):
    class Meta:
        model = CreateTests
        fields = '__all__'


