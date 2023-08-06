from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Table, Leg, Foot


def index(request):
    tables = Table.objects.all()
    return render(request, 'tables/index.html', { 'tables': tables })

def table(request, table_id):
    table = get_object_or_404(Table, pk=table_id) 
    legs = Leg.objects.filter(table_id = table_id)
    feet = Foot.objects.filter(legs__in = [1,2,3,4]).distinct()
    return render(request, 'tables/table.html', { 'table': table, 'legs': legs, 'feet': feet })

