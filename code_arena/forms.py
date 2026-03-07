from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import User, Problem, Example
class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    pfp = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["full_name", "university_id", "email", "password", "pfp"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@uap-bd.edu"):
            raise forms.ValidationError("Invalid email address")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")
        return email

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username.endswith("@uap-bd.edu"):
            raise forms.ValidationError("Invalid email address")
        return username
class ProblemForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Categories"
    )

class Meta:
    model = Problem
    fields = ['title', 'difficulty', 'time_limit', 'statement', 'input_specification', 'output_specification', 'categories']
ExampleFormSet = inlineformset_factory(
    Problem, Example,
    fields=['input', 'output', 'note'],
    extra=1,
    can_delete=True,
    widgets={
        'input': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        'output': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        'note': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
    }
)
