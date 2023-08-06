from django.urls import path, include
from . import views

app_name = 'tables'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:table_id>', views.table, name='table'),
]