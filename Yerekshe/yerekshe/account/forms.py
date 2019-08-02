from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo
from django.contrib.auth.forms import UserCreationForm

GENDER = (
    ('male', 'Male'),
    ('female', 'Female')
)

class Login(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password')



class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='first_name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'first name'}
    ), required=True, max_length=15)

    last_name = forms.CharField(label='last_name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'last name'}
    ), required=True, max_length=15)

    username = forms.CharField(label='username1', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username'}
    ), required=True, max_length=50)

    email = forms.CharField(label='email', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'email'}
    ), required=True, max_length=50)

    password = forms.CharField(label='password1', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'create a password'}
    ), required=True, max_length=50)

    confirm_password = forms.CharField(label='password2', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'confirm password'}
    ), required=True, max_length=50)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm password does not match")


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('profile_pic',)


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {'username': forms.TextInput(attrs={'readonly': 'True'})}




