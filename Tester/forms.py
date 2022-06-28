from django.forms import ModelForm
from Tester.models import UxTester, UploadVideo, FeedBack
class TesterForm(ModelForm):
    class Meta:
        model = UxTester
        fields = '__all__'


class UploadVideoForm(ModelForm):
    class Meta:
        model = UploadVideo
        fields = '__all__'


class UserDeleteForm(ModelForm):
    class Meta:
        model=UxTester
        fields=[]


class FeedbackForm(ModelForm):
    class Meta:
        model=FeedBack
        fields='__all__'        