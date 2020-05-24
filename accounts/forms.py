from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Account

Sex_Choices = [
    ('male', '남성'),
    ('Female', '여')
]

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit= True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user

class AccountForm(ModelForm):
    class Meta:
        model = Account
        sex = forms.CharField(label='성별', widget=forms.RadioSelect(choices=Sex_Choices))
        fields = ['name', 'age', 'wallet', 'sex']

