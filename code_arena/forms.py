from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import User, Problem, Example, Submission, Contest, ContestRegistration, ContestSubmission, Category
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
