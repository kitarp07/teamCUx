from django.forms import ModelForm
from Tester.models import UxTester, UploadVideo
class TesterForm(ModelForm):
    class Meta:
        model = UxTester
        fields = '__all__'


class UploadVideoForm(ModelForm):
    class Meta:
        model = UploadVideo
        fields = '__all__'