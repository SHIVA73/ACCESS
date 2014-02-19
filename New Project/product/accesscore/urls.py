from django.contrib import admin
from django.conf.urls import patterns, url, include
admin.autodiscover()
from django.conf import settings
from accesscore import views
from product import settings
try:
    print "i am in try"
    urlpatterns = patterns('accesscore.views',

    # login and authentication
        # (r'^login/$',views.login),# opens login page to provide login username and password
        # (r'^authent/$',views.authent), # authentication
        # (r'^forgetpwd/$',views.forgetpwd), # Enter mailid user name and password
        # (r'^getmail/$',views.getmail),# Get Username and password to his mail
        # (r'^Add_Person/$',views.Add_Person),
        # (r'^/Forms/Add_Company/$',Add_Company),
        url(r'^usermanagement/initialsetup/CompanyDetails/$','CompanyDetails'),
        url(r'^Forms/CompanyDetails/$','CompanyDetails'),
        url(r'^Forms/Edit_Company/(?P<id>\d+)/$','Edit_Company'),
        url(r'^Forms/Add_Company/$','Add_Company'),
        url(r'^Forms/Delete_Company/(?P<id>\d+)/$','Delete_Company'),
        
        url(r'^usermanagement/initialsetup/DepartmentDetails/$','DepartmentDetails'),
        url(r'^Forms/DepartmentDetails/$','DepartmentDetails'),
        url(r'^Forms/Edit_Department/(?P<id>\d+)/$','Edit_Department'),
        url(r'^Forms/Delete_Department/(?P<id>\d+)/$','Delete_Department'),
        url(r'^Forms/Add_Department/$','Add_Department'),
        
        url(r'^usermanagement/PersonDetails/$','PersonDetails'),
        url(r'^Forms/PersonDetails/$','PersonDetails'),
        url(r'^Forms/Edit_Person/(?P<id>\d+)/$','Edit_Person'),
        url(r'^Forms/Delete_Person/(?P<id>\d+)/$','Delete_Person'),
        url(r'^Forms/Add_Person/$','Add_Person'),
        
        url(r'^Forms/CardDetails/$','CardDetails'),
        url(r'^Forms/Edit_Card/(?P<id>\d+)/$','Edit_Card'),
        url(r'^Forms/Delete_Card/(?P<id>\d+)/$','Delete_Card'),
        url(r'^Forms/Add_Card/$','Add_Card'),
        
        url(r'^Forms/VehicleDetails/$','VehicleDetails'),
        url(r'^Forms/Edit_Vehicle/(?P<id>\d+)/$','Edit_Vehicle'),
        url(r'^Forms/Delete_Vehicle/(?P<id>\d+)/$','Delete_Vehicle'),
        url(r'^Forms/Add_Vehicle/$','Add_Vehicle'),
        
        url(r'^Forms/DeviceDetails/$','DeviceDetails'),
        url(r'^Forms/Edit_Device/(?P<id>\d+)/$','Edit_Device'),
        url(r'^Forms/Delete_Device/(?P<id>\d+)/$','Delete_Device'),
        url(r'^Forms/Add_Device/$','Add_Device'),
        
        url(r'^Forms/PersonTypeDetails/$','PersonTypeDetails'),
        url(r'^Forms/Edit_PersonType/(?P<id>\d+)/$','Edit_PersonType'),
        url(r'^Forms/Delete_PersonType/(?P<id>\d+)/$','Delete_PersonType'),
        url(r'^Forms/Add_PersonType/$','Add_PersonType'),
        
        url(r'^Forms/VehicleTypeDetails/$','VehicleTypeDetails'),
        url(r'^Forms/Edit_VehicleType/(?P<id>\d+)/$','Edit_VehicleType'),
        url(r'^Forms/Delete_VehicleType/(?P<id>\d+)/$','Delete_VehicleType'),
        url(r'^Forms/Add_VehicleType/$','Add_VehicleType'),
        
        url(r'^Forms/DeviceGroupDetails/$','DeviceGroupDetails'),
        url(r'^Forms/Edit_DeviceGroup/(?P<id>\d+)/$','Edit_DeviceGroup'),
        url(r'^Forms/Delete_DeviceGroup/(?P<id>\d+)/$','Delete_DeviceGroup'),
        url(r'^Forms/Add_DeviceGroup/$','Add_DeviceGroup'),
        
        url(r'^Forms/ScheduleDetails/$','ScheduleDetails'),
        url(r'^Forms/Edit_Schedule/(?P<id>\d+)/$','Edit_Schedule'),
        url(r'^Forms/Delete_Schedule/(?P<id>\d+)/$','Delete_Schedule'),
        url(r'^Forms/Add_Schedule/$','Add_Schedule'),
        
        url(r'^Forms/AccessGroupDetails/$','AccessGroupDetails'),
        url(r'^Forms/Edit_AccessGroup/(?P<id>\d+)/$','Edit_AccessGroup'),
        url(r'^Forms/Delete_AccessGroup/(?P<id>\d+)/$','Delete_AccessGroup'),
        url(r'^Forms/Add_AccessGroup/$','Add_AccessGroup'),
        
        url(r'^Forms/AccessGroupAssignedtoCardDetails/$','AccessGroupAssignedtoCardDetails'),
        url(r'^Forms/Edit_AccessGroupAssignedtoCard/(?P<id>\d+)/$','Edit_AccessGroupAssignedtoCard'),
        url(r'^Forms/Delete_AccessGroupAssignedtoCard/(?P<id>\d+)/$','Delete_AccessGroupAssignedtoCard'),
        url(r'^Forms/Add_AccessGroupAssignedtoCard/$','Add_AccessGroupAssignedtoCard'),
        
        url(r'^Forms/CardAccessorDetails/$','CardAccessorDetails'),
        url(r'^Forms/Edit_CardAccessor/(?P<id>\d+)/$','Edit_CardAccessor'),
        url(r'^Forms/Delete_CardAccessor/(?P<id>\d+)/$','Delete_CardAccessor'),
        url(r'^Forms/Add_CardAccessor/$','Add_CardAccessor'),
        
        url(r'^Forms/Feature_Form/$','FeatureForm'),
        url(r'^Forms/Edit_Feature_Form/(?P<id>\d+)/$','Edit_Feature_Form'),
        url(r'^Forms/Delete_Feature_Form/(?P<id>\d+)/$','Delete_Feature_Form'),
        url(r'^Forms/Add_Feature_Form/$','Add_Feature_Form'),
        
        url(r'^Forms/ListDetails/$','ListDetails'),
        url(r'^Forms/Edit_ListDetails/(?P<id>\d+)/$','Edit_ListDetails'),
        url(r'^Forms/Delete_ListDetails/(?P<id>\d+)/$','Delete_ListDetails'),
        url(r'^Forms/Add_ListDetails/$','Add_ListDetails'),
        
        url(r'^Reports/PersonDetails/$','PersonInfo'),
        url(r'^Reports/movement/today/$','Reports_movement_today'),
        url(r'^Reports/CustomReport/$','Reports_CustomReport'),
        url(r'^Reports/CustomReport_Fun/$','Reports_CustomReport_Fun'),
        url(r'^Reports/Blockwise_Report/$','Blockwise_Report'),
        url(r'^Reports/Blockwise_Report_Fun/$','Blockwise_Report_Fun'),
        url(r'^Reports/Devicewise_Report/$','Devicewise_Report'),
        url(r'^Reports/Devicewise_Report_Fun/$','Devicewise_Report_Fun'),
        url(r'^Reports/Expired_Cards/$','Expired_Cards'),
        url(r'^Reports/InvalidAccess/$','InvalidAccess'),
        url(r'^Reports/CardsGoingtoExpire/$','CardsGoingtoExpire'),
        url(r'^Reports/CardsGoingtoExpire_Fun/$','CardsGoingtoExpire_Fun'),
        
        url(r'^scan/$','scan'),
        url(r'^shiva/$','shiva'),
        
        
        # (r'^Add_Department/$',views.Add_Department),
        # (r'^Add_Card/$',views.Add_Card),
        
    # Logout    
        # (r'^logout/$',views.logout),#LOGOUT
        url(r'^admin/', include(admin.site.urls)),
    )
    urlpatterns += patterns('django.views.static',
            (r'mymedia/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
        )
except Exception:  
    print "i am in exception"
    