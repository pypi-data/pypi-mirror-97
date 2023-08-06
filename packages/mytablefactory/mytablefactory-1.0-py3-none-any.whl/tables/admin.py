from django.contrib import admin
from .models import Table, Leg, Foot

class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class LegAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class FootAdmin(admin.ModelAdmin):
    list_display = ('id', 'width', 'length', 'radius', 'legs_list') 
    def legs_list(self, obj):
        return ", ".join([str(p.id) for p in obj.legs.all()])

admin.site.register(Table, TableAdmin)
admin.site.register(Leg)
admin.site.register(Foot, FootAdmin)