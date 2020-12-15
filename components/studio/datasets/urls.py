from django.urls import path
from . import views

app_name = 'datasets'

urlpatterns = [
    path('<int:page_index>', views.page, name='page'),
    path('<str:path_name>/<int:page_index>', views.path_page, name='path_page'),
    #path('<int:page_index>/<str:entry_name>/datasheet', views.datasheet, name='datasheet'),
    path('<int:page_index>/<str:name>/datasheet/<str:action>', views.datasheet, name='datasheet'),
    path('<int:page_index>/<str:name>/submit', views.submit, name='submit')
]
