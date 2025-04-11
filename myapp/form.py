from django import forms
from django.core.validators import RegexValidator, EmailValidator
from .models import Payment

class PaymentForm(forms.ModelForm):
    email = forms.EmailField(
        validators=[EmailValidator(message="Enter a valid email address")],
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

    contact = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^[6-9]\d{9}$',
                message="Enter a valid 10-digit Indian mobile number starting with 6-9"
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your contact number'})
    )

    class Meta:
        model = Payment
        fields = [
            'full_name',
            'email',
            'contact',
            'category',
            'organisation_name',
            'job_title',
            'meals',
            'whatsapp_number',
            'additional_comments',
            'about_us'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your contact number'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'organisation_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter organisation name'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job title'}),
            'meals': forms.Select(attrs={'class': 'form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter WhatsApp number'}),
            'additional_comments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Any comments', 'rows': 3}),
            'about_us': forms.Select(attrs={'class': 'form-control'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        organisation_name = cleaned_data.get('organisation_name')
        job_title = cleaned_data.get('job_title')

        if organisation_name and not job_title:
            self.add_error('job_title', 'Job title is required if organisation name is provided')


