from django.contrib import admin
from django.conf.urls import patterns, url, include
admin.autodiscover()
from django.conf import settings
# from CLA import views
# from CoreLeaveApp import settings
try:
    print "i am in try"
    urlpatterns = patterns('leaveapp.views',

   
        # url(r'^Forms/EmployeeType/$','EmployeeTypeDetails'),
        # url(r'^Forms/Edit_EmployeeType/(?P<id>\d+)/$','Edit_EmployeeType'),
        # url(r'^Forms/Add_EmployeeType/$','Add_EmployeeType'),
        # url(r'^Forms/Delete_EmployeeType/(?P<id>\d+)/$','Delete_EmployeeType'),
        
        # url(r'^Forms/Employee/$','EmployeeDetails'),
        # url(r'^Forms/Edit_Employee/(?P<id>\d+)/$','Edit_Employee'),
        # url(r'^Forms/Add_Employee/$','Add_Employee'),
        # url(r'^Forms/Delete_Employee/(?P<id>\d+)/$','Delete_Employee'),
        
        url(r'^LM/LeaveType/$','LeaveTypeDetails'),
        url(r'^Edit_LeaveType/(?P<id>\d+)/$','Edit_LeaveType'),
        url(r'^Add_LeaveType/$','Add_LeaveType'),
        url(r'^Delete_LeaveType/(?P<id>\d+)/$','Delete_LeaveType'),
        
        url(r'^LM/LeaveSetup/$','LeaveSetupDetails'),
        url(r'^Add_LeaveSetup/$','Add_LeaveSetup'),
        url(r'^Edit_LeaveSetup/(?P<id>\d+)/$','Edit_LeaveSetup'),
        url(r'^Delete_LeaveSetup/(?P<id>\d+)/$','Delete_LeaveSetup'),
        
        url(r'^LM/LeaveApply/$','LeaveApplyDetails'),
        url(r'^Add_LeaveApply/$','Add_LeaveApply'),
        url(r'^Edit_LeaveApply/(?P<id>\d+)/$','Edit_LeaveApply'),
        url(r'^Delete_LeaveApply/(?P<id>\d+)/$','Delete_LeaveApply'),
        
        url(r'^LM/Approve/$','Approve'),
        url(r'^Edit_Approve/(?P<id>\d+)/$','Edit_Approve'),
        url(r'^Delete_Approve/(?P<id>\d+)/$','Delete_Approve'),
        
        url(r'^LM/Cancel/$','Cancel'),
        url(r'^Edit_Cancel/(?P<id>\d+)/$','Edit_Cancel'),
        url(r'^Delete_Cancel/(?P<id>\d+)/$','Delete_Cancel'),
		
		url(r'^LM/Compoff/$','Compoff'),
		url(r'^Add_Compoff/$','Add_Compoff'),
		
		# url(r'^Forms/ChangePassword/$','ChangePassword'),
		# url(r'^Forms/ChangePasswordFun/$','ChangePasswordFun'),
		
		url(r'^LM/ChangePassword/$','ChangePassword'),
		url(r'^Forms/ChangePasswordFun/$','ChangePasswordFun'),
		
		url(r'^Reports/LeaveBalance/$','LeaveBalance'),
        
       
        
       
      

        url(r'^admin/', include(admin.site.urls)),
    )
    urlpatterns += patterns('django.views.static',
            (r'mymedia/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
        )
except Exception:  
    print "i am in exception"
    