from django.contrib import admin
from timeandattendance.models import *

admin.site.register(shift_type)
admin.site.register(workday_schedule)
admin.site.register(shifttype_schedule_map)
admin.site.register(person_workday_schedule_map)

