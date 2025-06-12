from django import forms
from .models import OJ,CodeSubmission, TestCase, problemset
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class OJForm(forms.ModelForm):
    class Meta:
        model=OJ
        fields=['text','photo'] 
        


class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=('username','email','password1','password2')
        
        
LANGUAGE_CHOICES = [
    ("py", "Python"),
    ("c", "C"),
    ("cpp", "C++"),
]


class CodeSubmissionForm(forms.ModelForm):
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)

    class Meta:
        model = CodeSubmission
        fields = ["language", "code", "input_data"]
        


class CodeSubmitForm(forms.Form): 
    code = forms.CharField(
        label='Your Code',
        widget=forms.Textarea()
    )
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, initial='py', label='Language')
    
    
    
## new added

class ProblemSetForm(forms.ModelForm):
    class Meta:
        model = problemset
        fields = ['title', 'description', 'topic', 'input_data', 'expected_output']
        
class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['input_data', 'expected_output']