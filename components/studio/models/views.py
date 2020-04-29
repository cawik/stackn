import uuid
from django.shortcuts import render
from django.http import HttpResponseRedirect
from projects.models import Project
from reports.models import Report, ReportGenerator
from .models import Model
from .forms import ModelForm
from reports.forms import GenerateReportForm
from django.contrib.auth.decorators import login_required
from deployments.models import DeploymentDefinition, DeploymentInstance
import logging
from reports.helpers import populate_report_by_id, get_download_link

logger = logging.getLogger(__name__)


@login_required(login_url='/accounts/login')
def index(request, user, project):
    template = 'models_list.html'
    project = Project.objects.filter(slug=project).first()

    models = Model.objects.filter(project=project)
    deployments = DeploymentDefinition.objects.all()

    return render(request, template, locals())


@login_required(login_url='/accounts/login')
def create(request, user, project):
    template = 'models_upload.html'

    project = Project.objects.filter(slug=project).first()
    uid = uuid.uuid4()

    if request.method == 'POST':
        obj = None

        form = ModelForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()

            url = '/projects/{}/{}/models/{}'.format(user, project.slug, obj.pk)
        else:
            url = '/projects/{}/{}/models/'.format(user, project.slug)

        return HttpResponseRedirect(url)
    else:
        form = ModelForm()

        return render(request, template, locals())


@login_required(login_url='/accounts/login')
def details(request, user, project, id):
    project = Project.objects.filter(slug=project).first()
    template = 'models_details.html'
    model = Model.objects.filter(id=id).first()
    deployments = DeploymentInstance.objects.filter(model=model)

    return render(request, template, locals())


@login_required(login_url='/accounts/login')
def delete(request, user, project, id):
    template = 'model_confirm_delete.html'

    project = Project.objects.filter(slug=project).first()
    model = Model.objects.filter(id=id).first()

    if request.method == "POST":
        # TODO(desislava@scaleoutsystems.com): If the model has been deployed, remove the instance as well.

        model.delete()

        return HttpResponseRedirect('/projects/{}/{}/models/'.format(user, project.slug))

    return render(request, template, locals())


@login_required(login_url='/accounts/login')
def model_reports(request, user, project, id):
    template = 'model_reports.html'

    project = Project.objects.filter(slug=project).first()
    report_generators = ReportGenerator.objects.filter(project=project)
    model = Model.objects.filter(id=id).first()

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

            from reports.jobs import run_job

            run_job(instance)

            return HttpResponseRedirect('/projects/{}/{}/models/'.format(user, project.slug))
    else:
        form = GenerateReportForm()

    return render(request, template, locals())