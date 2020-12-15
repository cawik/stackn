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
    q1 = forms.CharField(max_length=500, required= False)
    q2 = forms.CharField(max_length=500, required= False)
    q3 = forms.CharField(max_length=500, required= False)
    q4 = forms.CharField(max_length=500, required= False)
    q5 = forms.CharField(max_length=500, required= False)
    q6 = forms.CharField(max_length=500, required= False)
    q7 = forms.CharField(max_length=500, required= False)
    q8 = forms.CharField(max_length=500, required= False)
    q9 = forms.CharField(max_length=500, required= False)
    q10 = forms.CharField(max_length=500, required= False)
    q11 = forms.CharField(max_length=500, required= False)
    q12 = forms.CharField(max_length=500, required= False)
    q13 = forms.CharField(max_length=500, required= False)
    q14 = forms.CharField(max_length=500, required= False)
    q15 = forms.CharField(max_length=500, required= False)
    q16 = forms.CharField(max_length=500, required= False)
    q17 = forms.CharField(max_length=500, required= False)

    class Meta:
        model = ModelCard
        fields = ('q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9','q10', 'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17')

    """
    c1 = forms.CharField(label=list(categories)[0], max_length=500, required= False)
    c2 = forms.CharField(label=list(categories)[1], max_length=500, required= False)
    c3 = forms.CharField(label=list(categories)[2], max_length=500, required= False)
    c4 = forms.CharField(label=list(categories)[3], max_length=500, required= False)
    c5 = forms.CharField(label=list(categories)[4], max_length=500, required= False)
    c6 = forms.CharField(label=list(categories)[5], max_length=500, required= False)

    q11 = forms.CharField(label=questions_1["q11"], max_length=500, required= False)
    q12 = forms.CharField(label=questions_1["q12"], max_length=500, required= False)
    q13 = forms.CharField(label=questions_1["q13"], max_length=500, required= False)
    q14 = forms.CharField(label=questions_1["q14"], max_length=500, required= False)
    q15 = forms.CharField(label=questions_1["q15"], max_length=500, required= False)
    q16 = forms.CharField(label=questions_1["q16"], max_length=500, required= False)
    q17 = forms.CharField(label=questions_1["q17"], max_length=500, required= False)
    q18 = forms.CharField(label=questions_1["q18"], max_length=500, required= False)
    q19 = forms.CharField(label=questions_1["q19"], max_length=500, required= False)

    q21 = forms.CharField(label=questions_2["q21"], max_length=500, required= False)
    q22 = forms.CharField(label=questions_2["q22"], max_length=500, required= False)
    q23 = forms.CharField(label=questions_2["q23"], max_length=500, required= False)


    q31 = forms.CharField(label=questions_3["q31"], max_length=500, required= False)
    q32 = forms.CharField(label=questions_3["q32"], max_length=500, required= False)

    q41 = forms.CharField(label=questions_4["q41"], max_length=500, required= False)
    q42 = forms.CharField(label=questions_4["q42"], max_length=500, required= False)
    q43 = forms.CharField(label=questions_4["q43"], max_length=500, required= False)

    q51 = forms.CharField(label=questions_5["q51"], max_length=500, required= False)

    q61 = forms.CharField(label=questions_6["q61"], max_length=500, required= False)

    
    class Meta:
        model = ModelCard
        fields = (
            'c1', 'c2', 'c3', 'c4','c5', 'c6', 
            'q11', 'q12','q13', 'q14', 'q15', 'q16','q17', 'q18', 'q19', 
            'q21', 'q22', 'q23', 
            'q31', 'q32',
            'q41', 'q42', 'q43',
            'q51',
            'q61'
        )
    """
