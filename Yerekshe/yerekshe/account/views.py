from django.shortcuts import render, redirect
from .forms import UserForm, UserProfileInfoForm, UpdateProfileForm
from django.contrib.auth import authenticate, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from . import forms

# from account.forms import RegistrationForm
# Create your views here.


def test(request):
    return render(request, 'test.html')

def home(request):
    return render(request, 'home.html')

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

        if registered:
            return HttpResponseRedirect(reverse('login'))

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'sign_up.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def login(request):
    if request.method == 'POST':
        form = forms.Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                return redirect('home')
            else:
                return redirect('login')
        else:
            return redirect('login')
    else:
        form = forms.Login()
        return render(request, 'login.html', {'form': form})

def report(request):
    return render(request, 'report.html')