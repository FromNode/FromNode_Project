from django import forms
from .models import Profile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','first_name','last_name']
        
# user의 기본 기능은 더 있습니다! 없을경우 profileform에 추가하기

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','location','birth_date']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']