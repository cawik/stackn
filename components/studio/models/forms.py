from django import forms
from .models import Model, ModelLog, Metadata, ModelCard

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
    
    model_detail_1 = forms.CharField(max_length=500, required=False)
    model_detail_2 = forms.CharField(max_length=500, required=False)
    model_detail_3 = forms.CharField(max_length=500, required=False)
    model_detail_4 = forms.CharField(max_length=500, required=False)
    model_detail_5 = forms.CharField(max_length=500, required=False)
    model_detail_6 = forms.CharField(max_length=500, required=False)
    model_detail_7 = forms.CharField(max_length=500, required=False)
    model_detail_8 = forms.CharField(max_length=500, required=False)

    intended_use_1 = forms.CharField(max_length=500, required=False)
    intended_use_2 = forms.CharField(max_length=500, required=False)
    intended_use_3 = forms.CharField(max_length=500, required=False)

    factor_1 = forms.CharField(max_length=500, required=False)
    factor_2 = forms.CharField(max_length=500, required=False)

    metric_1 = forms.CharField(max_length=500, required=False)
    metric_2 = forms.CharField(max_length=500, required=False)
    metric_3 = forms.CharField(max_length=500, required=False)

    ethical_consideration = forms.CharField(max_length=500, required=False)

    caveats_and_recommendations = forms.CharField(max_length=500, required=False)

    class Meta:
        model = ModelCard
        fields = (
                'model_detail_1', 'model_detail_2', 'model_detail_3', 'model_detail_4', 'model_detail_5', 'model_detail_6', 'model_detail_7', 'model_detail_8', 
                'intended_use_1', 'intended_use_2','intended_use_3', 
                'factor_1', 'factor_2', 
                'metric_1', 'metric_2', 'metric_3', 
                'ethical_consideration', 
                'caveats_and_recommendations'
        )
