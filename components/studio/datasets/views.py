from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, FileResponse, Http404
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
import ast
#from fpdf import FPDF

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


    """

    submitbutton = request.POST.get("submit")

    datasheet_info = {}
    print("Project:" , project.slug)
    form = DatasheetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            datasheet_file_upload = form.cleaned_data.get("upload")
            print(form.name)
            print("form is valid")
            if not datasheet_file_upload:
                print("no upload")
                #for i in range(0, len(questions) + 1):
                #    datasheet_info[questions[i]] = form.cleaned_data.get("q{}".format(str(i)))
                datasheet_info[questions[0]] = form.cleaned_data.get("q0")
                datasheet_info[questions[1]] = form.cleaned_data.get("q1")
                datasheet_info[questions[2]] = form.cleaned_data.get("q2")
                datasheet_info[questions[3]] = form.cleaned_data.get("q3")
                datasheet_info[questions[4]] = form.cleaned_data.get("q4")
                datasheet_info[questions[5]] = form.cleaned_data.get("q5")
                datasheet_info[questions[6]] = form.cleaned_data.get("q6")
                datasheet_info[questions[7]] = form.cleaned_data.get("q7")
                datasheet_info[questions[8]] = form.cleaned_data.get("q8")
                datasheet_info[questions[9]] = form.cleaned_data.get("q9")
                print(datasheet_info)
                #pdf = create_pdf(datasheet_info)
                #pdf.output("datasets/datasheets/datasheet_example.pdf")
                #datasheet_file = open("datasets/datasheets/datasheet_example.pdf", "rb")
                #pdf.output("datasheets/datasheet_{}.pdf".format(dataset_model.name))
                #datasheet_file = open("datasheets/datasheet_{}".format(dataset_model.name), "rb")
                #datasheet_file = open("datasets/test.txt", 'r')
                #dataset_model.datasheet = File(datasheet_file)
                #dataset_model.datasheet = File(datasheet_file)
                #dataset_model.save()
                #datasheet_file.close()
            else:
                print("upload")
                dataset.datasheet_upload = File(datasheet_file_upload)
                dataset.save()
            if Dataset.objects.filter(project=project.name, name=name):
                dataset = Dataset.objects.get(name=name)
            else:
                dataset = Dataset()
                dataset.name = name
                dataset.project = project.name
            dataset.datasheet = datasheet_info
            dataset.save()
        else:
            print("form not valid")
    """
    

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
            if 'pdf' in request.POST:
                print("Generating pdf...")
                pdf = create_pdf(datasheet_info, name)
                pdf.output('{}.pdf'.format(name))
                return pdf_view(request, '{}.pdf'.format(name))            
        else:
            print("Invalid form. Redirecting back to datasets...")
        return HttpResponseRedirect(
            reverse('datasets:page', kwargs={'user': request.user, 'project': project, 'page_index': 1}))
    return render(request, 'dataset_datasheet.html', locals())

def pdf_view(request, file):
    try:
        return FileResponse(open(file, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()
