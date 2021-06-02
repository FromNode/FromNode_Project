from django import forms
from UserApp.models import User


class UserListForm(forms.ModelForm):
    peer = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)
