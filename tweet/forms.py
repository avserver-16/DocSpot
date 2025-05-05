from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class TweetForm(forms.ModelForm):
    custom_category = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter custom category if selecting Other'
        })
    )

    class Meta:
        model = Tweet
        fields = ['name', 'file', 'category', 'custom_category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email", help_text="Must end with @svkmmumbai.onmicrosoft.com")
    sap_id= forms.IntegerField(required=True, label="SAP ID", help_text="Must be 11 characters long")
    admission_year = forms.IntegerField(required=True, label="Admission Year")
    graduation_year = forms.IntegerField(required=True, label="Graduation Year")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()  # Use the custom user model
        fields = ["username", "email", "sap_id", "admission_year", "graduation_year"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

