from django.contrib import admin
from .models import Predictions
from django import forms

# Register your models here.

class Prediction(admin.ModelAdmin):
    list_display = ('profile', 'age', 'gender', 'Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8','Q9','Q10','Q11', 'predicted_on', 'num')

admin.site.register(Predictions, Prediction)