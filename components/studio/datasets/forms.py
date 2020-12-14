from django import forms
from .datasheet_questions import questions

class DatasheetForm(forms.Form):
    q0 = forms.CharField(label=questions[0], max_length=500, widget=forms.Textarea({}), required= False)
    q1 = forms.CharField(label=questions[1], max_length=500, widget=forms.Textarea({}), required= False)
    q2 = forms.CharField(label=questions[2], max_length=500, widget=forms.Textarea({}), required= False)
    q3 = forms.CharField(label=questions[3], max_length=500, widget=forms.Textarea({}), required= False)
    q4 = forms.CharField(label=questions[4], max_length=500, widget=forms.Textarea({}), required= False)
    q5 = forms.CharField(label=questions[5], max_length=500, widget=forms.Textarea({}), required= False)
    q6 = forms.CharField(label=questions[6], max_length=500, widget=forms.Textarea({}), required= False)
    q7 = forms.CharField(label=questions[7], max_length=500, widget=forms.Textarea({}), required= False)
    q8 = forms.CharField(label=questions[8], max_length=500, widget=forms.Textarea({}), required= False)
    q9 = forms.CharField(label=questions[9], max_length=500, widget=forms.Textarea({}), required= False)
    upload = forms.FileField(label="Upload Datasheet", required=False)