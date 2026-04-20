from django import forms

from .models import HomePageContent, NewsSection


class NewsSectionForm(forms.ModelForm):
    class Meta:
        model = NewsSection
        fields = ['title', 'thumbnail', 'content', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 12, 'id': 'id_content'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class HomePageContentForm(forms.ModelForm):
    class Meta:
        model = HomePageContent
        fields = [
            'hero_title',
            'hero_description',
            'hero_button_text',
            'hero_button_url',
            'hero_image',
            'feature_1_title',
            'feature_1_description',
            'feature_2_title',
            'feature_2_description',
            'feature_3_title',
            'feature_3_description',
            'news_section_title',
            'news_section_subtitle',
        ]
        widgets = {
            'hero_title': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'hero_button_text': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_button_url': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'feature_1_title': forms.TextInput(attrs={'class': 'form-control'}),
            'feature_1_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'feature_2_title': forms.TextInput(attrs={'class': 'form-control'}),
            'feature_2_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'feature_3_title': forms.TextInput(attrs={'class': 'form-control'}),
            'feature_3_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'news_section_title': forms.TextInput(attrs={'class': 'form-control'}),
            'news_section_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
        }
