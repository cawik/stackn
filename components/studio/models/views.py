import uuid
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
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
from django.template import Context, Template
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
import tempfile
import ast
import os
from django.contrib.staticfiles import finders


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


def get_initial_data(form_entry, form_str, initial):
    counter = 1
    for key, value in form_entry.items():
        initial[form_str + '{}'.format(counter)] = value
        counter += 1
    return initial


def get_form_data(form, form_entry, form_str):
    card_entry = {}
    for i in range(0, len(form_entry)):
        question = form_entry[i]
        provided_answer = form.cleaned_data.get(form_str + '{}'.format(i+1))
        card_entry[question] = provided_answer
    return card_entry


@login_required
def model_card(request, user, project, id, action):
    template = 'create_card.html'
    project = Project.objects.get(slug=project)
    model = Model.objects.get(id=id)
    if action == 'create':
        has_card = False
        form = ModelCardForm()
    else:
        has_card = True
        model_card = ModelCard.objects.get(project=project.name, model=model.name, model_version=model.version)
        initial = {}
        initial = get_initial_data(ast.literal_eval(model_card.model_details), 'model_detail_', initial)
        initial = get_initial_data(ast.literal_eval(model_card.intended_uses), 'intended_use_', initial)
        initial = get_initial_data(ast.literal_eval(model_card.factors), 'factor_', initial)
        initial = get_initial_data(ast.literal_eval(model_card.metrics), 'metric_', initial)
        initial['ethical_consideration'] = model_card.ethical_consideration
        initial['caveats_and_recommendations'] = model_card.caveats_and_recommendations
        form = ModelCardForm(initial=initial)

    return render(request, template, locals())


@login_required
def submit(request, user, project, id, action):
    project = Project.objects.filter(slug=project).first()
    model = Model.objects.filter(id=id).first()
    if request.method == "POST":
        form = ModelCardForm(request.POST)
        if form.is_valid():
            print("Valid form! Saving")
            if action == 'update':
                print("A model card exists for current model. Updating existing model card...")
                model_card = ModelCard.objects.get(project=project.name, model=model.name, model_version=model.version)
                model_card.version = model_card.version + 1
            else:
                print("No model card exists for current model. Populating new model card...")
                model_card = ModelCard()
                model_card.model = model.name
                model_card.model_version = model.version
                model_card.project = project.name
            model_card.model_details = get_form_data(form, model_details, 'model_detail_')
            model_card.intended_uses = get_form_data(form, intended_use, 'intended_use_')
            model_card.factors = get_form_data(form, model_factors, 'factor_')
            model_card.metrics = get_form_data(form, model_metrics, 'metric_')
            model_card.ethical_consideration = form.cleaned_data.get('ethical_consideration')
            model_card.caveats_and_recommendations = form.cleaned_data.get('caveats_and_recommendations')
            model_card.save()
            print("Model card saved! Redirecting back to details page for {} {}".format(model.name, model.version))
        else:
            print("Invalid form. Redirecting back to details page for {} {}".format(model.name, model.version))
        return HttpResponseRedirect(
            reverse('models:details', kwargs={'user': user, 'project': project.slug, 'id': id}))
    return render(request, 'create_card.html', locals())

@login_required
def view_pdf(request, user, project, id):
    print('Generating pdf...')
    project = Project.objects.filter(slug=project).first()
    model = Model.objects.filter(id=id).first()


    card_object = ModelCard.objects.get(project=project.name, model=model.name, model_version=model.version)
    model_details = ast.literal_eval(card_object.model_details)
    intended_uses = ast.literal_eval(card_object.intended_uses)
    factors = ast.literal_eval(card_object.factors)
    metrics = ast.literal_eval(card_object.metrics)
    ethical_consideration = card_object.ethical_consideration
    caveats_and_recommendations = card_object.caveats_and_recommendations

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(model.name)
    response['Content-Transfer-Encoding'] = 'binary'

    font_config = FontConfiguration()
    css = CSS('./static/css/datasheet.css', font_config=font_config)

    html_string=render_to_string('modelcard_pdf_template.html', {'model_details': model_details, 'intended_uses': intended_uses, 'factors': factors, 'metrics': metrics, 'ethical_consideration': ethical_consideration, 'caveats_and_recommendations': caveats_and_recommendations, 'version': model.version, 'name': model.name})
    html = HTML(string=html_string)
    result = html.write_pdf(stylesheets=[css], font_config=font_config)

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response
