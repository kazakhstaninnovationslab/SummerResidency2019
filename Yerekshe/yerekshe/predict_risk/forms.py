from django import forms
from .models import Predictions

class Predict_Form(forms.ModelForm):
    class Meta:
        model = Predictions
        fields = ('age', 'gender', '')
        widgets = { 'age' : forms.TextInput(attrs={'class' : 'form-control'}),
                    'gender' : forms.Select(attrs={'class' : 'form-control'}),
                    }