from django import forms
from NodeApp.models import Nodes, Node_Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Node_Comment
        fields = ['content']
        labels = {
            'content': '내용',
        }
