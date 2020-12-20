import uuid
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from projects.models import Project, ProjectLog
from reports.models import Report, ReportGenerator
from .models import Model, ModelLog, Metadata, ModelCard
from .forms import ModelForm, ModelCardForm
from reports.forms import GenerateReportForm
from django.contrib.auth.decorators import login_required
from deployments.models import DeploymentDefinition, DeploymentInstance
import logging
from reports.helpers import populate_report_by_id, get_download_link
import markdown
import ast
from collections import defaultdict
from .model_cards_questions import model_details, intended_use, model_factors, model_metrics, ethical_considerations, model_caveats

new_data = defaultdict(list)
logger = logging.getLogger(__name__)


def index(request):
    models = Model.objects.filter(access='PU')

    return render(request, 'models_cards.html', locals())


@login_required
def list(request, user, project):
    template = 'models_list.html'
    project = Project.objects.filter(slug=project).first()

    models = Model.objects.filter(project=project)
    
    # model_logs = ModelLog.objects.all()

    # TODO: Filter by project and access.
    deployments = DeploymentDefinition.objects.all()

    return render(request, template, locals())


@login_required
def create(request, user, project):
    template = 'models_upload.html'

    project = Project.objects.filter(slug=project).first()
    uid = uuid.uuid4()

    if request.method == 'POST':
        obj = None

        form = ModelForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()

            l = ProjectLog(project=project, module='MO', headline='Model',
                           description='A new Model {name} has been added'.format(name=obj.name))
            l.save()

            url = '/{}/{}/models/{}'.format(user, project.slug, obj.pk)
        else:
            url = '/{}/{}/models/'.format(user, project.slug)

        return HttpResponseRedirect(url)
    else:
        form = ModelForm()

        return render(request, template, locals())


@login_required
def change_access(request, user, project, id):
    model = Model.objects.filter(pk=id).first()
    previous = model.get_access_display()

    if request.method == 'POST':
        visibility = request.POST.get('access', '')
        if visibility != model.access:
            model.access = visibility
            model.save()
            project_obj = Project.objects.get(slug=project)
            l = ProjectLog(project=project_obj, module='MO', headline='Model - {name}'.format(name=model.name),
                           description='Changed Access Level from {previous} to {current}'.format(previous=previous,
                                                                                                  current=model.get_access_display()))
            l.save()

    return HttpResponseRedirect(
        reverse('models:details', kwargs={'user': user, 'project': project, 'id': id}))


@login_required
def details(request, user, project, id):
    project = Project.objects.filter(slug=project).first()
    model = Model.objects.filter(id=id).first()
    model_access_choices = ['PU', 'PR', 'LI']
    model_access_choices.remove(model.access)
    #has_card = ModelCard.objects.filter(project=project.name, model=model.name, model_version=model.version)
    deployments = DeploymentInstance.objects.filter(model=model)

    report_generators = ReportGenerator.objects.filter(project=project)

    unfinished_reports = Report.objects.filter(status='P').order_by('created_at')
    for report in unfinished_reports:
        populate_report_by_id(report.id)

    reports = Report.objects.filter(model__id=id, status='C').order_by('-created_at')

    report_dtos = []
    for report in reports:
        report_dtos.append({
            'id': report.id,
            'description': report.description,
            'created_at': report.created_at,
            'filename': get_download_link(project.pk, 'report_{}.json'.format(report.id))
        })

    if request.method == 'POST':
        file_path = None
        form = GenerateReportForm(request.POST)
        if form.is_valid():
            generator_id = int(form.cleaned_data['generator_file'])
            generator_object = ReportGenerator.objects.filter(pk=generator_id).first()

            file_path = 'reports/{}'.format(generator_object.generator)

            instance = {
                'id': str(uuid.uuid4()),
                'path_to_file': file_path,
                'model_uid': model.uid,
                'project_name': project.slug
            }

            new_report = Report(model=model, report="", job_id=instance['id'], generator=generator_object, status='P')
            new_report.save()

            l = ProjectLog(project=project, module='MO', headline='Model - {name}'.format(name=model.name),
                           description='Newly generated Metrics #{id}'.format(id=new_report.pk))
            l.save()

            from reports.jobs import run_job

            run_job(instance)

            return HttpResponseRedirect('/{}/{}/models/'.format(user, project.slug))
    else:
        form = GenerateReportForm()

    log_objects = ModelLog.objects.filter(project=project.name, trained_model=model)
    model_logs = []
    for log in log_objects:
        model_logs.append({
            'id': log.id,
            'trained_model': log.trained_model,
            'training_status': log.training_status,
            'training_started_at': log.training_started_at,
            'execution_time': log.execution_time,
            'code_version': log.code_version,
            'current_git_repo': log.current_git_repo,
            'latest_git_commit': log.latest_git_commit,
            'system_details': ast.literal_eval(log.system_details),
            'cpu_details': ast.literal_eval(log.cpu_details)
        })

    md_objects = Metadata.objects.filter(project=project.name, trained_model=model)
    if md_objects:
        metrics = get_chart_data(md_objects)

    try:
        model_card = ModelCard.objects.get(project=project.name, model=model, model_version=model.version)
        model_details = ast.literal_eval(model_card.model_details)
        intended_uses = ast.literal_eval(model_card.intended_uses)
        model_factors = ast.literal_eval(model_card.factors)
        model_metrics = ast.literal_eval(model_card.metrics)
        ethical_considerations = model_card.ethical_consideration
        model_caveats = model_card.caveats_and_recommendations
    except Exception as e:
        print("No model card has been created for this model.")

    filename = None
    readme = None
    import requests as r
    url = 'http://{}-file-controller/models/{}/readme'.format(project.slug, model.name)
    try:
        response = r.get(url)
        if response.status_code == 200 or response.status_code == 203:
            payload = response.json()
            if payload['status'] == 'OK':
                filename = payload['filename']

                md = markdown.Markdown(extensions=['extra'])
                readme = md.convert(payload['readme'])
    except Exception as e:
        logger.error("Failed to get response from {} with error: {}".format(url, e))

    return render(request, 'models_details.html', locals())


def get_chart_data(md_objects):
    new_data.clear()
    metrics_pre = []
    metrics = []
    for md_item in md_objects:
        metrics_pre.append({
            'run_id': md_item.run_id,
            'metrics': ast.literal_eval(md_item.metrics),
            'parameters': ast.literal_eval(md_item.parameters)
        })
    for m in metrics_pre: 
        for key, value in m["metrics"].items():
            new_data[key].append([m["run_id"], value, m["parameters"]])
    for key, value in new_data.items():
        data = []
        labels = []
        params = []
        run_id = []
        run_counter = 0
        for item in value:
            run_counter += 1
            labels.append("Run {}".format(run_counter))
            run_id.append(item[0])
            data.append(item[1])
            params.append(item[2])
        metrics.append({
            "metric": key,
            "details": {
                "run_id": run_id,
                "labels": labels,
                "data": data,
                "params": params
            }
        })
    return metrics


def details_public(request, id):
    model = Model.objects.filter(pk=id).first()
    deployments = DeploymentInstance.objects.filter(model=model)

    reports = Report.objects.filter(model__pk=id, status='C').order_by('-created_at')
    report_dtos = []
    for report in reports:
        report_dtos.append({
            'id': report.id,
            'description': report.description,
            'created_at': report.created_at,
            'filename': get_download_link(model.project.pk, 'report_{}.json'.format(report.id))
        })

    filename = None
    readme = None
    import requests as r
    url = 'http://{}-file-controller/models/{}/readme'.format(model.project.slug, model.name)
    try:
        response = r.get(url)
        if response.status_code == 200 or response.status_code == 203:
            payload = response.json()
            if payload['status'] == 'OK':
                filename = payload['filename']

                md = markdown.Markdown(extensions=['extra'])
                readme = md.convert(payload['readme'])
    except Exception as e:
        logger.error("Failed to get response from {} with error: {}".format(url, e))

    return render(request, 'models_details_public.html', locals())


@login_required
def delete(request, user, project, id):
    template = 'model_confirm_delete.html'

    project = Project.objects.get(slug=project)
    model = Model.objects.get(id=id)

    if request.method == "POST":
        l = ProjectLog(project=project, module='MO', headline='Model',
                       description='Model {name} has been removed'.format(name=model.name))
        l.save()

        model.delete()

        return HttpResponseRedirect(reverse('models:list', kwargs={'user':user, 'project':project.slug}))

    return render(request, template, locals())


@login_required
def card(request, user, project, id, action):
    template = 'card.html'
    project = Project.objects.get(slug=project)
    model = Model.objects.get(id=id)
    if action == 'create':
        has_card = False
        initial = {}
        form = ModelCardForm()
    
    elif action == 'update':
        has_card = True
        initial = {}
        db_entry = ModelCard.objects.get(project=project.name, model=model.name, model_version=model.version)
        model_details = ast.literal_eval(db_entry.model_details)
        intended_use = ast.literal_eval(db_entry.intended_uses)
        model_factors = ast.literal_eval(db_entry.factors)
        model_metrics = ast.literal_eval(db_entry.metrics)
        ethical_consideration = db_entry.ethical_consideration
        model_caveats = db_entry.caveats_and_recommendations

        counter = 1
        for key, value in model_details.items():
            initial['md_{}'.format(counter)] = value
            counter += 1
        
        counter = 1
        for key, value in intended_use.items():
            initial['iu_{}'.format(counter)] = value
            counter += 1
        
        counter = 1
        for key, value in model_factors.items():
            initial['f_{}'.format(counter)] = value
            counter += 1
        
        counter = 1
        for key, value in model_metrics.items():
            initial['m_{}'.format(counter)] = value
            counter += 1
        
        initial['ec'] = ethical_consideration
        initial['cr'] = model_caveats

        form = ModelCardForm(initial=initial)

    return render(request, template, locals())


@login_required
def submit(request, user, project, id):
    project = Project.objects.filter(slug=project).first()
    model = Model.objects.filter(id=id).first()
    card_entry_1 = {}
    card_entry_2 = {}
    card_entry_3 = {}
    card_entry_4 = {}
    card_entry_5 = {}
    card_entry_6 = {}
    if request.method == "POST":
        form = ModelCardForm(request.POST)
        if form.is_valid():
            print("Valid form! Saving")
            for i in range(0, len(model_details)):
                question = model_details[i]
                provided_answer = form.cleaned_data.get("md_{}".format(i+1))
                card_entry_1[question] = provided_answer

            for i in range(0, len(intended_use)):
                question = intended_use[i]
                provided_answer = form.cleaned_data.get("iu_{}".format(i+1))
                card_entry_2[question] = provided_answer

            for i in range(0, len(model_factors)):
                question = model_factors[i]
                provided_answer = form.cleaned_data.get("f_{}".format(i+1))
                card_entry_3[question] = provided_answer

            for i in range(0, len(model_metrics)):
                question = model_metrics[i]
                provided_answer = form.cleaned_data.get("m_{}".format(i+1))
                card_entry_4[question] = provided_answer
            try: 
                card_object = ModelCard.objects.get(project=project.name, model=model.name, model_version=model.version)
                print("A model card exists for current model. Updating existing model card...")
            except Exception as e:
                print("Error '{}' raised since no model card exists for current model. Populating a new model card...".format(e))
                card_object = ModelCard()
                card_object.model = model.name
                card_object.model_version = model.version
                card_object.project = project.name
            card_object.model_details = card_entry_1
            card_object.intended_uses = card_entry_2
            card_object.factors = card_entry_3
            card_object.metrics = card_entry_4
            card_object.ethical_consideration = form.cleaned_data.get("ec")
            card_object.caveats_and_recommendations = form.cleaned_data.get("cr")
            card_object.save()
            print(form)
            print("Model card saved for {} {}".format(model.name, model.version))
        else:
            print("Invalid form. Redirecting back to models...")
        return HttpResponseRedirect(
            reverse('models:details', kwargs={'user': user, 'project': project.slug, 'id': id}))
    return render(request, 'card.html', locals())
