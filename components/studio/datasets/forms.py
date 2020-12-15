from django import forms
from .models import Dataset
#from .datasheet_questions import datasheet_questions

class DatasheetForm(forms.Form):
    q1 = forms.CharField(max_length=500, required= False)
    q2 = forms.CharField(max_length=500, required= False)
    q3 = forms.CharField(max_length=500, required= False)
    q4 = forms.CharField(max_length=500, required= False)
    q5 = forms.CharField(max_length=500, required= False)
    q6 = forms.CharField(max_length=500, required= False)
    q7 = forms.CharField(max_length=500, required= False)
    q8 = forms.CharField(max_length=500, required= False)
    q9 = forms.CharField(max_length=500, required= False)
    upload = forms.FileField(label="Upload Datasheet", required=False)
    class Meta:
        model = Dataset
        fields = ('q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9')