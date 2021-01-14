from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, FileResponse, Http404, HttpResponse
from django.core.files import File
from projects.models import Project
from studio.minio import MinioRepository, ResponseError
from django.conf import settings as sett
from projects.helpers import get_minio_keys
from .forms import DatasheetForm
from .helpers import create_pdf
from .models import Dataset
from .datasheet_questions import datasheet_questions
from django.urls import reverse
#from io import BytesIO
#from xhtml2pdf import pisa
from django.template import Context, Template
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
import tempfile
import ast

import os
#from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
#from fpdf import FPDF
#from .utils import render_to_pdf

@login_required
def page(request, user, project, page_index):
    template = 'dataset_page.html'
    project = Project.objects.filter(slug=project).first()
    url_domain = sett.DOMAIN

    minio_keys = get_minio_keys(project)
    decrypted_key = minio_keys['project_key']
    decrypted_secret = minio_keys['project_secret']

    datasets = []
    try:
        minio_repository = MinioRepository('{}-minio:9000'.format(project.slug), decrypted_key,
                                           decrypted_secret)

        objects = minio_repository.client.list_objects_v2('dataset')
        for obj in objects:
            datasets.append({'is_dir': obj.is_dir,
                             # remove '/' after the directory name
                             'name': obj.object_name[:-1] if obj.is_dir else obj.object_name,
                             'size': round(obj.size / 1000000, 2),
                             'location': 'minio',
                             'modified': obj.last_modified})
        for idx, dataset in enumerate(datasets):
            if dataset['is_dir']:
                continue
            try: 
                db_entry = Dataset.objects.get(project=project.slug, name=dataset['name'])
                if db_entry and db_entry.datasheet:
                    dataset['datasheet'] = True
                else:
                    dataset['datasheet'] = False
            except Exception as err:
                print(err)
                dataset['datasheet'] = False
            datasets[idx] = dataset
        
    except ResponseError as err:
        print(err)
    previous_page = 1
    next_page = 1
    if len(datasets) > 0:
        import math
        # allow 10 rows per page in the table
        pages = list(map(lambda x: x + 1, range(math.ceil(len(datasets) / 10))))

        datasets = datasets[page_index * 10 - 10:page_index * 10]

        previous_page = page_index if page_index == 1 else page_index - 1
        next_page = page_index if page_index == pages[-1] else page_index + 1

    return render(request, template, locals())


@login_required
def path_page(request, user, project, path_name, page_index):
    template = 'dataset_path_page.html'
    project = Project.objects.filter(slug=project).first()
    url_domain = sett.DOMAIN

    minio_keys = get_minio_keys(project)
    decrypted_key = minio_keys['project_key']
    decrypted_secret = minio_keys['project_secret']

    datasets = []
    try:
        minio_repository = MinioRepository('{}-minio:9000'.format(project.slug), decrypted_key,
                                           decrypted_secret)

        objects = minio_repository.client.list_objects_v2('dataset', recursive=True)
        for obj in objects:
            if obj.object_name.startswith(path_name + '/'):
                datasets.append({'is_dir': obj.is_dir,
                                 'name': obj.object_name.replace(path_name + '/', ''),
                                 'size': round(obj.size / 1000000, 2),
                                 'modified': obj.last_modified})

        import math
        pages = list(map(lambda x: x + 1, range(math.ceil(len(datasets) / 10))))
    except ResponseError as err:
        print(err)
    datasets = datasets[page_index * 10 - 10:page_index * 10]

    previous_page = page_index if page_index == 1 else page_index - 1
    next_page = page_index if page_index == pages[-1] else page_index + 1

    return render(request, template, locals())


@login_required
def datasheet(request, user, project, page_index, name, action):
    template = 'dataset_datasheet.html'
    project = Project.objects.filter(slug=project).first()
    questions = datasheet_questions
    if action == 'details':
        print('details')
        has_datasheet = True
        db_entry = Dataset.objects.get(project=project.slug, name=name)
        datasheet = ast.literal_eval(db_entry.datasheet)
    elif action == 'create':
        has_datasheet = False

    else:
        initial = {}
        db_entry = Dataset.objects.get(project=project.slug, name=name)
        datasheet = ast.literal_eval(db_entry.datasheet)
        counter = 1
        for key, value in datasheet.items():
            initial['q{}'.format(counter)] = value
            counter += 1
        form = DatasheetForm(initial=initial)
        print(form)
    return render(request, template, locals())

    

@login_required
def submit(request, user, project, page_index, name):
    datasheet_info = {}
    if request.method == "POST":
        form = DatasheetForm(request.POST)
        if form.is_valid():
            print("Valid form! Saving")
            for i in range(0, len(datasheet_questions)):
                question = datasheet_questions[i]
                provided_answer = form.cleaned_data.get("q{}".format(i+1))
                datasheet_info[question] = provided_answer
            if Dataset.objects.filter(project=project, name=name):
                dataset = Dataset.objects.get(name=name)
            else:
                dataset = Dataset()
                dataset.name = name
                dataset.project = project
            dataset.datasheet = datasheet_info
            dataset.save()
            print(request.POST)  
        else:
            print("Invalid form. Redirecting back to datasets...")
        #if 'pdf' in request.POST:
            #print("Generating pdf...")
            #dataset_context = {"project": project, 'name': name, 'datasheet': datasheet_info }
            #pdf = render_to_pdf('datasheet_pdf_template.html', dataset_context)
            #print(pdf)
            #dataset.fpdf = pdf
            #dataset.save()
            #pdf = render_pdf_view(request, 'datasheet_pdf_template.html', dataset_context)
            #return render(request, pdf)
            #print(pdf)   
        return HttpResponseRedirect(
            reverse('datasets:page', kwargs={'user': request.user, 'project': project, 'page_index': 1}))
    return render(request, 'dataset_datasheet.html', locals())

@login_required
def view_pdf(request, user, project, page_index, name):
    print('Generating pdf...')
    db_entry = Dataset.objects.get(project=project, name=name)
    datasheet = ast.literal_eval(db_entry.datasheet)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(db_entry.name)
    response['Content-Transfer-Encoding'] = 'binary'

    font_config = FontConfiguration()
    css = CSS('./static/css/datasheet.css', font_config=font_config)

    html_string=render_to_string('datasheet_pdf_template.html', {'datasheet': datasheet, 'name': name})
    html = HTML(string=html_string)
    result = html.write_pdf(stylesheets=[css], font_config=font_config)

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response

    