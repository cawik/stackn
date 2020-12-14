from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.files import File
from projects.models import Project
from studio.minio import MinioRepository, ResponseError
from django.conf import settings as sett
from projects.helpers import get_minio_keys
from .forms import DatasheetForm
from .helpers import create_pdf, upload_file
from .models import Dataset
from .datasheet_questions import questions
from fpdf import FPDF

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

#@login_required
#def datasheet(request, user, project):
    #template = 'dataset_datasheet.html'
    """
    project = Project.objects.filter(slug=project).first()
    url_domain = sett.DOMAIN

    minio_keys = get_minio_keys(project)
    decrypted_key = minio_keys['project_key']
    decrypted_secret = minio_keys['project_secret']
    """

    #return render(request, template, locals())

@login_required
def datasheet(request, user, project, page_index, name):
    template = 'dataset_datasheet.html'
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
                             'datasheet': 'datasheet',
                             'size': round(obj.size / 1000000, 2),
                             'location': 'minio',
                             'modified': obj.last_modified})

    except ResponseError as err:
        print(err)

    submitbutton = request.POST.get("submit")

    datasheet_info = {}
    print("Project:" , project.slug)
    form = DatasheetForm(request.POST or None)
    if Dataset.objects.filter(project=project.name, name=name):
        dataset = Dataset.objects.get(name=name)
        print(dataset.dvc_etag)
    else:
        print("else")
        dataset = Dataset()
    #dataset_model = Dataset(request.POST or None)

    if form.is_valid():
        datasheet_file_upload = form.cleaned_data.get("upload")
        print("form is valid")
        if not datasheet_file_upload:
            print("no upload")
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
            dataset.name = name
            dataset.project = project.name
            dataset.datasheet = datasheet_info
            dataset.save()
            pdf = create_pdf(datasheet_info)
            pdf.output("datasets/datasheets/datasheet_example.pdf")
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
    else:
        print("form not valid")

        

 
    """    
    submitbutton = request.POST.get("submit")

    datasheet_info = []

    form = DatasheetForm(request.POST or None)
    if form.is_valid():
        uploaded = None
        datasheet_info.append(form.cleaned_data.get("q1"))
        datasheet_info.append(form.cleaned_data.get("q2")
        #uploaded = form.cleaned_data.get("upload")
        #if uploaded == None:
        #create_pdf(q, datasheet_info, "test")
        
    previous_page = 1
    next_page = 1
    if len(datasets) > 0:
        import math
        # allow 10 rows per page in the table
        pages = list(map(lambda x: x + 1, range(math.ceil(len(datasets) / 10))))

        datasets = datasets[page_index * 10 - 10:page_index * 10]

        previous_page = page_index if page_index == 1 else page_index - 1
        next_page = page_index if page_index == pages[-1] else page_index + 1
    """
    return render(request, template, locals())



"""
def datasheet(request, user, project, page_index):
    template = 'dataset_datasheet.html'
    if request.method == 'POST':
        form = DatasheetForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/submitted')
    else:
        form = DatasheetForm()

    return render(request, template, {'form': form})
"""