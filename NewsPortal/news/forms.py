from django import forms
from django.core.validators import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['id',
                'post_author',
                'title',
                'text'

        ]