from django import forms
from .models import  *
from django.utils.translation import ugettext_lazy 

class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = ['group','text', "image"]
        widgets = {
            'text':forms.Textarea(attrs={'class': 'form-control', 'rows':6})
        }
        labels = {
            'group': ugettext_lazy('Выерите категорию:'),
            'text': ugettext_lazy('Текст поста:')
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = ['text']