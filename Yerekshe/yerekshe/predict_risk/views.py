from django.shortcuts import render, redirect, get_object_or_404
import csv, io
from .forms import Predict_Form
from .models import UserProfileInfo
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,permission_required
from django.urls import reverse
from django.contrib import messages




# Create your views here.
