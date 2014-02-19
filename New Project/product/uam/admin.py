'''
Created on Oct 26, 2012

@author: god
'''
from django.contrib import admin
import models
from django.db.models import Q

admin.site.register(models.product)
admin.site.register(models.roles)
# admin.site.register(models.Country)

class myuser(admin.ModelAdmin):
    # list_filter = ['created_date']
    def formfield_for_dbfield(self,db_field,**kwargs):
        print "dfdff"
        if db_field.name == "Password":
            print "admin",self
        return super(myuser, self).formfield_for_dbfield(db_field,  **kwargs)    
admin.site.register(models.user,myuser)

class MyModelAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            print "hi"
            kwargs["queryset"] = models.menu.objects.filter(~Q(type='F'))
        return super(MyModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(models.menu,MyModelAdmin)

admin.site.register(models.role_to_menu)
class userrole(admin.ModelAdmin):
    list_filter = ['created_date']
    search_fields = ['Role_id__Role_Name']
    
admin.site.register(models.user_role_map,userrole)
# admin.site.register(models.aabc)
# admin.site.register(models.bc)
# admin.site.register(models.Feature_Group)
# admin.site.register(models.Feature_Subgroup)
# admin.site.register(models.Feature_Items)
# admin.site.register(models.Role_TO_Feature_Map)
# admin.site.register(models.Role_FGroup_FSubGroup_FItems_Map)
# admin.site.register(models.Role_Feature_Group_Map)



# class UserAdmin(admin.ModelAdmin):
    # print "g"
# admin.site.register(models.sm_user,UserAdmin)