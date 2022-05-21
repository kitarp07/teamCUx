from django.forms import ModelForm
from Tester.models import UxTester
class TesterForm(ModelForm):
    class Meta:
        model = UxTester
        fields = '__all__'