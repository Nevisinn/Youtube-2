from django import forms
from .models import Videos, Comments


class CustomForm(forms.ModelForm):
    class Meta:
        model = Videos
        exclude = ['url', 'author', 'view_count']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
        }


class VideoSearchForm(forms.Form):
    query = forms.CharField(label='Поиск', max_length=100)

    def clean_query(self):
        query = self.cleaned_data['query']
        return query
