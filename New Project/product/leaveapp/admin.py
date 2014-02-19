from django.contrib import admin
from leaveapp.models import *
# from models import *

admin.site.register(holiday)
admin.site.register(leavetype)
admin.site.register(leavesetup)
admin.site.register(leaveapply)
admin.site.register(comp_off)