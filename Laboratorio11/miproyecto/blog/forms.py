from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'categories']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Título',
            'content': 'Contenido',
            'image': 'Imagen',
            'categories': 'Categorías',
        }