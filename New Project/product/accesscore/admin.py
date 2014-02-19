from django.contrib import admin
from uam.models import *
from models import *

class person_admin(admin.ModelAdmin):
    search_fields = ['userid']
class vehicle_admin(admin.ModelAdmin):
    search_fields = ['vehicle_number']

admin.site.register(company)
admin.site.register(department)
admin.site.register(person_type)
admin.site.register(person,person_admin)
admin.site.register(vehicle_type)
admin.site.register(vehicle,vehicle_admin)
admin.site.register(accessor)
admin.site.register(card)
admin.site.register(card_to_accessor_map)
admin.site.register(device)
admin.site.register(schedule)
admin.site.register(devicegroup)
# admin.site.register(Accessgroupdefinition)
admin.site.register(accessgroup)
admin.site.register(accessgroupassigntocard)
admin.site.register(movement)
admin.site.register(com_entity)
admin.site.register(com_feature_fields)
admin.site.register(com_feature_field_values)
admin.site.register(com_list)


