from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'thumbnail', 'excerpt', 'content', 'tags', 'status', 'featured']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'excerpt': forms.Textarea(attrs={'rows': 3}),
        }
