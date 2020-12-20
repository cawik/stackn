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
    # md as in "Model Details"; represents the questions defined in model_details in model_cards_questions.py
    md_1 = forms.CharField(max_length=500, required=False)
    md_2 = forms.CharField(max_length=500, required=False)
    md_3 = forms.CharField(max_length=500, required=False)
    md_4 = forms.CharField(max_length=500, required=False)
    md_5 = forms.CharField(max_length=500, required=False)
    md_6 = forms.CharField(max_length=500, required=False)
    md_7 = forms.CharField(max_length=500, required=False)

    # iu as in "Intended Uses"; represents the questions defined in intended_use in model_cards_questions.py
    iu_1 = forms.CharField(max_length=500, required=False)
    iu_2 = forms.CharField(max_length=500, required=False)
    iu_3 = forms.CharField(max_length=500, required=False)

    # f as in "Factors"; represents the questions defined in factors in model_cards_questions.py
    f_1 = forms.CharField(max_length=500, required=False)
    f_2 = forms.CharField(max_length=500, required=False)

    # m as in "Metrics"; represents the questions defined in metrics in model_cards_questions.py
    m_1 = forms.CharField(max_length=500, required=False)
    m_2 = forms.CharField(max_length=500, required=False)
    m_3 = forms.CharField(max_length=500, required=False)

    # ec as in "Ethical Considerations"; represents the questions defined in metrics in model_cards_questions.py
    ec = forms.CharField(max_length=500, required=False)

    # cr as in "Caveats and Recommendations"; represents the questions defined in metrics in model_cards_questions.py
    cr = forms.CharField(max_length=500, required=False)

    class Meta:
        model = ModelCard
        fields = (
                'md_1', 'md_2', 'md_3', 'md_4', 'md_5', 'md_6', 'md_7', 
                'iu_1', 'iu_2','iu_3', 
                'f_1', 'f_2', 
                'm_1', 'm_2', 'm_3', 
                'ec', 
                'cr'
        )
