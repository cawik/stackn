from django import forms
from .models import Model, ModelLog, Metadata, ModelCard
#from .model_cards_questions import categories, questions_1, questions_2, questions_3, questions_4, questions_5, questions_6

class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ('uid', 'name', 'description', 'url', 'project')
        widgets = {
            'uid': forms.HiddenInput(),
            'project': forms.HiddenInput()
        }

class ModelLogForm(forms.ModelForm):
    class Meta:
        model = ModelLog
        fields = (
            'run_id', 'trained_model', 'project', 'training_started_at', 'execution_time', 'code_version',
            'current_git_repo', 'latest_git_commit', 'system_details', 'cpu_details', 'training_status')

class Metadata(forms.ModelForm):
    class Meta:
        model = Metadata
        fields = (
            'run_id', 'trained_model', 'project', 'model_details', 'parameters', 'metrics')


class ModelCardForm(forms.ModelForm):
    q1 = forms.CharField(max_length=500, required=False)
    q2 = forms.CharField(max_length=500, required=False)
    q3 = forms.CharField(max_length=500, required=False)
    q4 = forms.CharField(max_length=500, required=False)
    q5 = forms.CharField(max_length=500, required=False)
    q6 = forms.CharField(max_length=500, required=False)
    q7 = forms.CharField(max_length=500, required=False)
    q8 = forms.CharField(max_length=500, required=False)
    q9 = forms.CharField(max_length=500, required=False)
    q10 = forms.CharField(max_length=500, required=False)
    q11 = forms.CharField(max_length=500, required=False)
    q12 = forms.CharField(max_length=500, required=False)
    q13 = forms.CharField(max_length=500, required=False)
    q14 = forms.CharField(max_length=500, required=False)
    q15 = forms.CharField(max_length=500, required=False)
    q16 = forms.CharField(max_length=500, required=False)
    q17 = forms.CharField(max_length=500, required=False)

    class Meta:
        model = ModelCard
        fields = ('q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9','q10', 'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17')
