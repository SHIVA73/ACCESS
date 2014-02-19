# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response,HttpResponseRedirect
from accesscore.models import *
from uam.models import *
from forms import *
from django import forms
from django.db.models import Q
from django.core.mail import *
from datetime import datetime,timedelta
import datetime
from django.db import connection


# def EmployeeTypeDetails(request):
    # pname = request.session['projectname']
    # level = request.session['level'] 
    # rolefeatures = request.session['Rolefetures']
    # username = request.session['username']
    # user = request.session['userid']
    # Data = EmployeeType.objects.all()
    # msg = "Please check the details"
    # txn_list = []
    # try: 
        # Did = request.session['id']
        # obj = EmployeeType.objects.get(id = Did)
        # name = obj.name
        # del request.session['id']
        # msg = 'EmployeeType ' +name+' Successfully Edited'    
    # except Exception:
        # pass
    # try:
        # Newid = request.session['txn.id']
        # obj = EmployeeType.objects.get(id = Newid)
        # name = obj.name
        # del request.session['txn.id']
        # msg = 'EmployeeType ' +name+' Successfully Added'
    # except Exception:
        # pass
    # try:
        # delete = request.session['deleteid']
        # obj = EmployeeType.objects.all().values('id')
        # if delete not in obj:
            # del request.session['deleteid']
            # msg = 'EmployeeType Successfully Deleted'
    # except Exception:
        # pass
    # try:
        # msg = request.session['message']
        # del request.session['message']
    # except Exception:
        # pass
    # for i in range(len(Data)):
        # dic = {}
        # dic['id'] = Data[i].id
        # dic['name'] = Data[i].name
        # dic['code'] = Data[i].code
        # dic['description'] = Data[i].description
        # txn_list.append(dic)
    # title = "EmployeeType List"
    # return render_to_response('LeaveApp/EmployeeTypeDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
# def Edit_EmployeeType(request,id):
    # pname = request.session['projectname']
    # rolefeatures = request.session['Rolefetures']
    # user = request.session['userid']
    # username = request.session['username']
    # Action_url = '/LeaveApp/Forms/Edit_EmployeeType/'+id+'/'
    # Cancel_url = '/LeaveApp/Forms/EmployeeType/'
    # title = 'Edit EmployeeType'
    # txnreport = EmployeeType.objects.get(id = id)
    # form = EmployeeTypeform(instance=txnreport)
    # if request.method == 'POST':
        # form = EmployeeTypeform(request.POST, instance=txnreport)
        # if EmployeeTypeform(instance=txnreport).has_changed():
            # request.session['id'] = id
        # if form.is_valid():
            # txn = form.save()
            # return HttpResponseRedirect('/LeaveApp/Forms/EmployeeType')
    # else:
        # form = EmployeeTypeform(instance=txnreport)    
    # return render_to_response('LeaveApp/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
# def Delete_EmployeeType(request,id):
    # try:
        # f = EmployeeType.objects.filter(id=id).delete()
        # request.session['deleteid'] = id
        # return HttpResponseRedirect('/LeaveApp/Forms/EmployeeType') 
    # except Exception:
        # message = "Cannot Delete EmployeeType,it is used in another table"
        # request.session['message'] = message
        # return HttpResponseRedirect('/LeaveApp/Forms/EmployeeType') 
# def Add_EmployeeType(request):
    # pname = request.session['projectname']
    # rolefeatures = request.session['Rolefetures']
    # user = request.session['userid']
    # username = request.session['username']
    # Action_url = '/LeaveApp/Forms/Add_EmployeeType/'
    # Cancel_url = '/LeaveApp/Forms/EmployeeType/'
    # title = 'Add EmployeeType'
    # if request.method == 'POST':
        # form = EmployeeTypeform(request.POST)
        # if form.is_valid():
            # txn = form.save()
            # return HttpResponseRedirect('/LeaveApp/Forms/EmployeeType')
    # else:
        # form = EmployeeTypeform()
    # return render_to_response('LeaveApp/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
    
# def EmployeeDetails(request):
    # pname = request.session['projectname']
    # level = request.session['level'] 
    # rolefeatures = request.session['Rolefetures']
    # username = request.session['username']
    # user = request.session['userid']
    # Data = person.objects.all()
    # msg = "Please check the details"
    # txn_list = []
    # try: 
        # Did = request.session['id']
        # obj = person.objects.get(id = Did)
        # name = obj.name
        # del request.session['id']
        # msg = 'Employee ' +name+' Successfully Edited'    
    # except Exception:
        # pass
    # try:
        # Newid = request.session['txn.id']
        # obj = person.objects.get(id = Newid)
        # name = obj.name
        # del request.session['txn.id']
        # msg = 'Employee ' +name+' Successfully Added'
    # except Exception:
        # pass
    # try:
        # delete = request.session['deleteid']
        # obj = person.objects.all().values('id')
        # if delete not in obj:
            # del request.session['deleteid']
            # msg = 'Employee Successfully Deleted'
    # except Exception:
        # pass
    # try:
        # msg = request.session['message']
        # del request.session['message']
    # except Exception:
        # pass
    # for i in range(len(Data)):
        # dic = {}
        # dic['id'] = Data[i].id
        # dic['name'] = Data[i].name
        # dic['code'] = Data[i].code
        # dic['description'] = Data[i].description
        # dic['dateofjoining'] = Data[i].dateofjoining
        # dic['userid'] = Data[i].userid
        # dic['employeetype'] = Data[i].employeetype
        # dic['approver'] = Data[i].approver
        # txn_list.append(dic)
    # title = "Employee List"
    # return render_to_response('LeaveApp/EmployeeDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
# def Edit_Employee(request,id):
    # pname = request.session['projectname']
    # rolefeatures = request.session['Rolefetures']
    # user = request.session['userid']
    # username = request.session['username']
    # Action_url = '/LeaveApp/Forms/Edit_Employee/'+id+'/'
    # Cancel_url = '/LeaveApp/Forms/Employee/'
    # title = 'Edit Employee'
    # txnreport = person.objects.get(id = id)
    # form = Employeeform(instance=txnreport)
    # if request.method == 'POST':
        # form = Employeeform(request.POST, instance=txnreport)
        # if Employeeform(instance=txnreport).has_changed():
            # request.session['id'] = id
        # if form.is_valid():
            # txn = form.save()
            # return HttpResponseRedirect('/LeaveApp/Forms/Employee')
    # else:
        # form = Employeeform(instance=txnreport)    
    # return render_to_response('LeaveApp/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
# def Delete_Employee(request,id):
    # try:
        # f = person.objects.filter(id=id).delete()
        # request.session['deleteid'] = id
        # return HttpResponseRedirect('/LeaveApp/Forms/Employee') 
    # except Exception:
        # message = "Cannot Delete Employee,it is used in another table"
        # request.session['message'] = message
        # return HttpResponseRedirect('/LeaveApp/Forms/Employee') 
# def Add_Employee(request):
    # pname = request.session['projectname']
    # rolefeatures = request.session['Rolefetures']
    # user = request.session['userid']
    # username = request.session['username']
    # Action_url = '/LeaveApp/Forms/Add_Employee/'
    # Cancel_url = '/LeaveApp/Forms/Employee/'
    # title = 'Add Employee'
    # if request.method == 'POST':
        # form = Employeeform(request.POST)
        # if form.is_valid():
            # txn = form.save()
            # return HttpResponseRedirect('/LeaveApp/Forms/Employee')
    # else:
        # form = Employeeform()
    # return render_to_response('LeaveApp/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
    
def LeaveTypeDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    user = request.session['userid']
    Data = leavetype.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = leavetype.objects.get(id = Did)
        name = obj.name
        del request.session['id']
        msg = 'LeaveType ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = leavetype.objects.get(id = Newid)
        name = obj.name
        del request.session['txn.id']
        msg = 'LeaveType ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = leavetype.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'LeaveType Successfully Deleted'
    except Exception:
        pass
    try:
        msg = request.session['message']
        del request.session['message']
    except Exception:
        pass
    for i in range(len(Data)):
        dic = {}
        dic['id'] = Data[i].id
        dic['name'] = Data[i].name
        dic['code'] = Data[i].code
        dic['description'] = Data[i].description
        txn_list.append(dic)
    title = "LeaveType List"
    return render_to_response('LeaveApp/LeaveTypeDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
    
def Edit_LeaveType(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/LeaveApp/Edit_LeaveType/'+id+'/'
    Cancel_url = '/LeaveApp/LM/LeaveType/'
    title = 'Edit LeaveType'
    txnreport = leavetype.objects.get(id = id)
    form = LeaveTypeform(instance=txnreport)
    if request.method == 'POST':
        form = LeaveTypeform(request.POST, instance=txnreport)
        if LeaveTypeform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save()
            return HttpResponseRedirect('/LeaveApp/LM/LeaveType')
    else:
        form = LeaveTypeform(instance=txnreport)    
    return render_to_response('LeaveApp/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_LeaveType(request,id):
    try:
        f = leavetype.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        return HttpResponseRedirect('/LeaveApp/LM/LeaveType') 
    except Exception:
        message = "Cannot Delete LeaveType,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/LeaveApp/LM/LeaveType') 
def Add_LeaveType(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/LeaveApp/Add_LeaveType/'
    Cancel_url = '/LeaveApp/LM/LeaveType/'
    title = 'Add LeaveType'
    if request.method == 'POST':
        form = LeaveTypeform(request.POST)
        if form.is_valid():
            txn = form.save()
            return HttpResponseRedirect('/LeaveApp/LM/LeaveType')
    else:
        form = LeaveTypeform()
    return render_to_response('LeaveApp/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
    
def LeaveSetupDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    user = request.session['userid']
    Data = leavesetup.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = leavesetup.objects.get(id = Did)
        name = obj.name
        del request.session['id']
        msg = 'LeaveSetup ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = leavesetup.objects.get(id = Newid)
        name = obj.name
        del request.session['txn.id']
        msg = 'LeaveSetup ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = leavesetup.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'LeaveSetup Successfully Deleted'
    except Exception:
        pass
    try:
        msg = request.session['message']
        del request.session['message']
    except Exception:
        pass
    for i in range(len(Data)):
        dic = {}
        dic['id'] = Data[i].id
        dic['leavetype'] = Data[i].leavetype
        dic['persontype'] = Data[i].persontype
        dic['numberofdays'] = Data[i].numberofdays
        dic['description'] = Data[i].description
        txn_list.append(dic)
    title = "LeaveSetup List"
    return render_to_response('LeaveApp/LeaveSetupDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
    
def Edit_LeaveSetup(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/LeaveApp/Edit_LeaveSetup/'+id+'/'
    Cancel_url = '/LeaveApp/LM/LeaveSetup/'
    title = 'Edit LeaveSetup'
    txnreport = leavesetup.objects.get(id = id)
    form = LeaveSetupform(instance=txnreport)
    if request.method == 'POST':
        form = LeaveSetupform(request.POST, instance=txnreport)
        if LeaveSetupform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save()
            return HttpResponseRedirect('/LeaveApp/LM/LeaveSetup')
    else:
        form = LeaveSetupform(instance=txnreport)    
    return render_to_response('LeaveApp/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_LeaveSetup(request,id):
    try:
        f = leavesetup.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        return HttpResponseRedirect('/LeaveApp/LM/LeaveSetup') 
    except Exception:
        message = "Cannot Delete Leave Setup,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/LeaveApp/LM/LeaveSetup') 
def Add_LeaveSetup(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/LeaveApp/Add_LeaveSetup/'
    Cancel_url = '/LeaveApp/LM/LeaveSetup/'
    title = 'Add LeaveSetup'
    if request.method == 'POST':
        form = LeaveSetupform(request.POST)
        if form.is_valid():
            txn = form.save()
            return HttpResponseRedirect('/LeaveApp/LM/LeaveSetup')
    else:
        form = LeaveSetupform()
    return render_to_response('LeaveApp/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
    
def LeaveApplyDetails(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    user = request.session['userid']
    roleid = request.session['roleid']
    role = roles.objects.get(id = roleid)
    if role.role_name == 'Employee':
        print "!!!!!!!!"
        emp = person.objects.filter(user_id = user)
        Data = leaveapply.objects.filter(person_id = emp)
        print "#",Data
    if role.role_name == 'leave admin':
        Data = leaveapply.objects.all()
    if role.role_name == 'Manager':
        emp = person.objects.get(user_id = user)
        emp1 = person.objects.filter(manager = emp.id)
        a = [str(i.id) for i in emp1]
        a.append(str(emp.id))
        Data = leaveapply.objects.filter(person_id__in = a)
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = leaveapply.objects.get(id = Did)
        name = obj.name
        del request.session['id']
        msg = 'LeaveApply ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = leaveapply.objects.get(id = Newid)
        name = obj.name
        del request.session['txn.id']
        msg = 'LeaveApply ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = leaveapply.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'LeaveApply Successfully Deleted'
    except Exception:
        pass
    try:
        msg = request.session['message']
        del request.session['message']
    except Exception:
        pass
    for i in range(len(Data)):
        dic = {}
        dic['id'] = Data[i].id
        dic['person'] = Data[i].person
        dic['startdate'] = Data[i].startdate
        dic['enddate'] = Data[i].enddate
        dic['numberofdays'] = Data[i].numberofdays
        dic['description'] = Data[i].description
        # dic['status'] = Data[i].status
        dic['status'] = dict(STATUS_CHOICES).get(Data[i].status)
        txn_list.append(dic)
    title = "LeaveApply List"
    return render_to_response('LeaveApp/LeaveApplyDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
    
def Edit_LeaveApply(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/LeaveApp/Edit_LeaveApply/'+id+'/'
    Cancel_url = '/LeaveApp/LM/LeaveApply/'
    title = 'Edit LeaveApply'
    txnreport = leaveapply.objects.get(id = id)
    form = LeaveApplyform(instance=txnreport)
    if request.method == 'POST':
        form = LeaveApplyform(request.POST, instance=txnreport)
        if LeaveApplyform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save()
            return HttpResponseRedirect('/LeaveApp/LM/LeaveApply')
    else:
        form = LeaveApplyform(instance=txnreport)    
    return render_to_response('LeaveApp/Edit_LeaveApply.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_LeaveApply(request,id):
    try:
        f = leaveapply.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        return HttpResponseRedirect('/LeaveApp/LM/LeaveApply') 
    except Exception:
        message = "Cannot Delete Leave Setup,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/LeaveApp/LM/LeaveApply') 

def Add_LeaveApply(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    usrid = request.session['userid']
    username = request.session['username']
    print "SSSSSSSSSS",usrid
    cursor = connection.cursor()
    cursor.execute('select isnull(sum(numberofdays),0) as nods from leaveapp_leavesetup ls \
        inner join accesscore_person_type et on ls.persontype_id = et.id\
        inner join accesscore_person ee on ee.persontype_id =  et.id where ee.user_id = \'%s\''%(usrid))
    p = cursor.fetchone()
    print "@@@@@@@",p[0]
    cursor.execute('select isnull(sum(numberofdays),0) as leavestaken from leaveapp_leaveapply la\
        inner join accesscore_person ce on ce.id = la.person_id where ce.user_id = \'%s\' and la.status in (0,1)'%(usrid))
    k = cursor.fetchone()
    print "#######",k[0]
    cursor.execute('select isnull(sum(numberofdays),0) as compoff from leaveapp_comp_off cco \
        inner join accesscore_person ce on ce.id = cco.person_id where ce.user_id = \'%s\''%(usrid))
    j = cursor.fetchone()
    print "&&&&&&&",j[0]
    Action_url = '/LeaveApp/Add_LeaveApply/'
    Cancel_url = '/LeaveApp/LM/LeaveApply/'
    title = 'Add LeaveApply'
    if request.method == 'POST':
        form = LeaveApplyform(request.POST)
        form.fields['person'] = forms.ModelChoiceField(person.objects.filter(user_id = usrid))
        try:
            mdate1 = datetime.datetime.strptime(request.POST['enddate'], "%Y-%m-%d").date()
            rdate1 = datetime.datetime.strptime(request.POST['startdate'], "%Y-%m-%d").date()
            daydiff = mdate1.weekday() - rdate1.weekday()
            delta = ((mdate1-rdate1).days - daydiff) / 7 * 5 + min(daydiff,5)
        except Exception:
            pass
        if form.is_valid():
            txn = form.save(commit = False)
            if p[0] != 0 and k[0] - j[0] != p[0] and float(p[0]) - (k[0] - j[0]) >= float(delta+1):    
                print "#$##########%#"
                txn.numberofdays = float(delta+1)
                txn.save()
                fromaddress = person.objects.get(user_id = usrid)
                from1 = fromaddress.primary_email
                print "AAAAAAA",fromaddress.manager_id
                App = user.objects.get(id = fromaddress.manager_id)
                Approver = person.objects.get(id = App.id)
                # appid = person.objects.get(id = App.id)
                # toaddress = person.objects.get(id = appid.approver)
                # toaddress1 = user.objects.get(id = toaddress.userid)
                to = Approver.primary_email
                print "##############",from1,to
                email = EmailMessage('Leave Request',str(request.POST['description']+"\n\n"+"Leave form "+request.POST['startdate']+" to "+request.POST['enddate']+"\n\n"+"Total Days:"+str(txn.numberofdays)+"\n\n"+"Mail From: "+from1+"\n\n"+"Approver:"+Approver.first_name), settings.EMAIL_HOST_USER,[to],settings.APPROVERS,headers={'Cc': ','.join(settings.APPROVERS)})
                email.send()
                return HttpResponseRedirect('/LeaveApp/LM/LeaveApply')
            else:
                print "SSSSSSSSSS"
                message = "Your Have "+str(float(p[0]) - (k[0] - j[0]))+" Leaves"
                request.session['message'] = message
                return HttpResponseRedirect('/LeaveApp/LM/LeaveApply')
    else:
        form = LeaveApplyform()
        form.fields['person'] = forms.ModelChoiceField(person.objects.filter(user_id = usrid))
    return render_to_response('LeaveApp/LeaveApply.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title,'tot':p[0],'applied':k[0] - j[0]})
    
def Approve(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    user = request.session['userid']
    roleid = request.session['roleid']
    role = roles.objects.get(id = roleid)
    msg = "Please check the details"
    txn_list = []
    if role.role_name == 'Employee':
        emp = person.objects.filter(user_id = user)
        Data = leaveapply.objects.filter(person_id = emp)
    if role.role_name == 'leave admin':
        Data = leaveapply.objects.all()
    if role.role_name == 'Manager':
        emp = person.objects.get(user_id = user)
        emp1 = person.objects.filter(manager = emp.id)
        Data = leaveapply.objects.filter(person_id__in = emp1)
    try: 
        Did = request.session['id']
        obj = leaveapply.objects.get(id = Did)
        name = obj.name
        del request.session['id']
        msg = 'LeaveApply ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = leaveapply.objects.get(id = Newid)
        name = obj.name
        del request.session['txn.id']
        msg = 'LeaveApply ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = leaveapply.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'LeaveApply Successfully Deleted'
    except Exception:
        pass
    try:
        msg = request.session['message']
        del request.session['message']
    except Exception:
        pass
    for i in range(len(Data)):
        dic = {}
        dic['id'] = Data[i].id
        dic['person'] = Data[i].person
        dic['startdate'] = Data[i].startdate
        dic['enddate'] = Data[i].enddate
        dic['numberofdays'] = Data[i].numberofdays
        dic['description'] = Data[i].description
        dic['status'] = dict(STATUS_CHOICES).get(Data[i].status)
        # dic['status'] = Data[i].status
        txn_list.append(dic)
    title = "Approve/Reject"
    return render_to_response('LeaveApp/ApproveDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
    
def Edit_Approve(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    usrid = request.session['userid']
    username = request.session['username']
    Action_url = '/LeaveApp/Edit_Approve/'+id+'/'
    Cancel_url = '/LeaveApp/LM/Approve/'
    title = 'Edit Approve'
    txnreport = leaveapply.objects.get(id = id)
    form = Approverform(instance=txnreport)
    if request.method == 'POST':
        form = Approverform(request.POST,instance=txnreport)
        form.fields['numberofdays'].widget.attrs['readonly'] = True
        form.fields['person'].widget.attrs['readonly'] = True
        form.fields['startdate'].widget.attrs['disabled'] = True
        form.fields['enddate'].widget.attrs['disabled'] = True
        form.fields['description'].widget.attrs['readonly'] = True
        if Approverform(instance=txnreport).has_changed():
            request.session['id'] = id
        code11 = form['status'].value()
        leaveapply.objects.filter(id=id).update(status=code11)
        fromaddress = person.objects.get(user_id = usrid)
        from1 = fromaddress.primary_email
        toaddress = person.objects.get(id = request.POST['person'])
        # toaddress1 = user.objects.get(id = toaddress.userid)
        tomail = toaddress.primary_email
        if code11 == '1':
            email = EmailMessage('Leave Request',"Approved"+"\n\n"+"Mail From: "+from1, settings.EMAIL_HOST_USER,[tomail],settings.APPROVERS,headers={'Cc': ','.join(settings.APPROVERS)})
            email.send()
        if code11 == '3':
            email = EmailMessage('Leave Request',"Rejected"+"\n\n"+"Mail From: "+from1, settings.EMAIL_HOST_USER,[tomail],settings.APPROVERS,headers={'Cc': ','.join(settings.APPROVERS)})
            email.send()
        return HttpResponseRedirect('/LeaveApp/LM/Approve')
    else:
        form = Approverform(instance=txnreport)
        form.fields['numberofdays'].widget.attrs['readonly'] = True
        form.fields['person'].widget.attrs['readonly'] = True
        form.fields['startdate'].widget.attrs['disabled'] = True
        form.fields['enddate'].widget.attrs['disabled'] = True
        form.fields['description'].widget.attrs['readonly'] = True   
    return render_to_response('LeaveApp/Edit_LeaveApply.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
    
def Delete_Approve(request,id):
    try:
        f = leaveapply.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        return HttpResponseRedirect('/LeaveApp/LM/Approve') 
    except Exception:
        message = "Cannot Delete Leave Approve,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/LeaveApp/LM/Approve') 
        
def Cancel(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    user = request.session['userid']
    roleid = request.session['roleid']
    role = roles.objects.get(id = roleid)
    emp = person.objects.filter(user_id = user)
    if role.role_name == 'Employee':
        Data = leaveapply.objects.filter(person_id = emp,status = 0)
    if role.role_name == 'leave admin':
        Data = leaveapply.objects.filter(status = 0)
    if role.role_name == 'Manager':
        emp = person.objects.get(user_id = user)
        Data = leaveapply.objects.filter(person_id = emp,status = 0)
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = leaveapply.objects.get(id = Did)
        name = obj.name
        del request.session['id']
        msg = 'LeaveApply ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = leaveapply.objects.get(id = Newid)
        name = obj.name
        del request.session['txn.id']
        msg = 'LeaveApply ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = leaveapply.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'LeaveApply Successfully Deleted'
    except Exception:
        pass
    try:
        msg = request.session['message']
        del request.session['message']
    except Exception:
        pass
    for i in range(len(Data)):
        dic = {}
        dic['id'] = Data[i].id
        dic['person'] = Data[i].person
        dic['startdate'] = Data[i].startdate
        dic['enddate'] = Data[i].enddate
        dic['numberofdays'] = Data[i].numberofdays
        dic['description'] = Data[i].description
        dic['status'] = dict(STATUS_CHOICES).get(Data[i].status)
        # dic['status'] = Data[i].status
        txn_list.append(dic)
    title = "Cancel"
    return render_to_response('LeaveApp/CancelDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
    
def Edit_Cancel(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    usrid = request.session['userid']
    username = request.session['username']
    Action_url = '/LeaveApp/Edit_Cancel/'+id+'/'
    Cancel_url = '/LeaveApp/LM/Cancel/'
    title = 'Edit Cancel'
    txnreport = leaveapply.objects.get(id = id)
    form = Cancelform(instance=txnreport)
    if request.method == 'POST':
        form = Cancelform(request.POST,instance=txnreport)
        form.fields['numberofdays'].widget.attrs['readonly'] = True
        form.fields['person'].widget.attrs['readonly'] = True
        form.fields['startdate'].widget.attrs['disabled'] = True
        form.fields['enddate'].widget.attrs['disabled'] = True
        form.fields['description'].widget.attrs['readonly'] = True
        if Cancelform(instance=txnreport).has_changed():
            request.session['id'] = id
        code11 = form['status'].value()
        leaveapply.objects.filter(id=id).update(status=code11)
        fromaddress = person.objects.get(user_id = usrid)
        from1 = fromaddress.primary_email
        App = user.objects.get(id = fromaddress.manager_id)
        Approver = person.objects.get(id = App.id)
        # appid = person.objects.get(id = App.id)
        # toaddress = person.objects.get(id = appid.approver)
        # toaddress1 = user.objects.get(id = toaddress.userid)
        to = Approver.primary_email
        if code11 == '2':
            email = EmailMessage('Leave Cancellation',"Cancelled"+"\n\n"+"Mail From: "+from1, settings.EMAIL_HOST_USER,[to],settings.APPROVERS,headers={'Cc': ','.join(settings.APPROVERS)})
            email.send()
        return HttpResponseRedirect('/LeaveApp/LM/Cancel')
    else:
        form = Cancelform(instance=txnreport)
        form.fields['numberofdays'].widget.attrs['readonly'] = True
        form.fields['person'].widget.attrs['readonly'] = True
        form.fields['startdate'].widget.attrs['disabled'] = True
        form.fields['enddate'].widget.attrs['disabled'] = True
        form.fields['description'].widget.attrs['readonly'] = True   
    return render_to_response('LeaveApp/Edit_LeaveApply.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})

def Delete_Cancel(request,id):
    try:
        f = leaveapply.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        return HttpResponseRedirect('/LeaveApp/LM/Cancel') 
    except Exception:
        message = "Cannot Delete Leave Cancel,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/LeaveApp/LM/Cancel') 
        
def Compoff(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    user = request.session['userid']
    roleid = request.session['roleid']
    role = roles.objects.get(id = roleid)
    emp = person.objects.filter(personid = user)
    Data = comp_off.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = comp_off.objects.get(id = Did)
        name = obj.name
        del request.session['id']
        msg = 'Comp Off ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = comp_off.objects.get(id = Newid)
        name = obj.name
        del request.session['txn.id']
        msg = 'Comp Off ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = comp_off.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Comp Off Successfully Deleted'
    except Exception:
        pass
    try:
        msg = request.session['message']
        del request.session['message']
    except Exception:
        pass
    for i in range(len(Data)):
        dic = {}
        dic['id'] = Data[i].id
        dic['personid'] = Data[i].person
        dic['numberofdays'] = Data[i].numberofdays
        dic['createdby'] = Data[i].createdby
        txn_list.append(dic)
    title = "Comp Off"
    return render_to_response('LeaveApp/CompoffDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
    
def Add_Compoff(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    usid = request.session['userid']
    print "#######",usid
    username = request.session['username']
    Action_url = '/LeaveApp/Add_Compoff/'
    Cancel_url = '/LeaveApp/LM/Compoff/'
    title = 'Add LeaveSetup'
    created = user.objects.get(id = usid)
    # craetedby = person.objects.get(user_id = created.id)
    # print "createdby.name",craetedby.name
    if request.method == 'POST':
        form = Compoff_form(request.POST)
        if form.is_valid():
            txn = form.save()
            return HttpResponseRedirect('/LeaveApp/LM/Compoff')
    else:
        form = Compoff_form(initial = {'createdby':created.first_name})
    return render_to_response('LeaveApp/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
    
def ChangePassword(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    usid = request.session['userid']
    username = request.session['username']
    return render_to_response('LeaveApp/ChangePassword.html',{'Rolefetures':rolefeatures,'projectname':pname,'username':username})
    
def ChangePasswordFun(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    usid = request.session['userid']
    username = request.session['username']
    pwd=request.POST['pwd']
    pwd1=request.POST['pwd1']
    from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)
    p = user.objects.get(id__exact = usid)
    if user.objects.get(id__exact = usid) and p.check_password(pwd):
        loginobj = user.objects.get(id = usid)
        loginobj.password = pwd1
        loginobj.save()
        return render_to_response('LeaveApp/user_response.html',{'Rolefetures':rolefeatures,'projectname':pname,'username':username,'msg':'Password has been changed successfully','link':'uam/home'})
    else:
       return render_to_response('LeaveApp/user_response.html',{'Rolefetures':rolefeatures,'projectname':pname,'username':username,'msg':'Wrong password','link':'LeaveApp/Forms/ChangePassword'})  
       
def LeaveBalance(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    usrid = request.session['userid']
    username = request.session['username']
    txn_list = []
    roleid = request.session['roleid']
    role = roles.objects.get(id = roleid)
    if role.role_name == 'Employee':
        Data = person.objects.filter(user_id = usrid)
    if role.role_name == 'HR':
        Data = person.objects.all()
    if role.role_name == 'Manager':
        emp = person.objects.get(user_id = usrid)
        emp1 = person.objects.filter(manager = emp.id)
        a = [str(i.userid) for i in emp1]
        a.append(str(emp.userid))
        Data = person.objects.filter(userid__in = a)
        print "SSSSSSSSSS",Data
    # for i in person.objects.all():
    for i in Data:
        print i
        # for p in leavesetup.objects.raw('select ls.id,coalesce(sum(numberofdays),0) as nods from LeaveApp_leavesetup ls \
            # inner join LeaveApp_employeetype et on ls.employeetype_id = et.id\
            # inner join LeaveApp_employee ee on ee.employeetype_id =  et.id where ee.userid = \'%s\''%(i.userid)):
            # pass
        # for k in leaveapply.objects.raw('select coalesce(sum(numberofdays),0) as leavestaken,la.id from LeaveApp_LeaveApply la\
            # inner join LeaveApp_employee ce on ce.id = la.employee_id where ce.userid = \'%s\' and la.status in (0,1)'%(i.userid)):
            # pass
        # for j in comp_off.objects.raw('select cco.id,coalesce(sum(numberofdays),0) as compoff from LeaveApp_comp_off cco \
            # inner join LeaveApp_employee ce on ce.id = cco.empid_id where ce.userid = \'%s\''%(i.userid)):
            # pass
        cursor = connection.cursor()
        cursor.execute('select isnull(sum(numberofdays),0) as nods from leaveapp_leavesetup ls \
            inner join accesscore_person_type et on ls.persontype_id = et.id\
            inner join accesscore_person ee on ee.persontype_id =  et.id where ee.user_id = \'%s\''%(i.user_id))
        p = cursor.fetchone()
        print "@@@@@@@",p[0]
        cursor.execute('select isnull(sum(numberofdays),0) as leavestaken from leaveapp_leaveapply la\
            inner join accesscore_person ce on ce.id = la.person_id where ce.user_id = \'%s\' and la.status in (0,1)'%(i.user_id))
        k = cursor.fetchone()
        print "#######",k[0]
        cursor.execute('select isnull(sum(numberofdays),0) as compoff from leaveapp_comp_off cco \
            inner join accesscore_person ce on ce.id = cco.person_id where ce.user_id = \'%s\''%(i.user_id))
        j = cursor.fetchone()
        print "&&&&&&&",j[0]
        dic = {}
        dic['employee'] = i.first_name
        dic['totalleaves'] = p[0]
        dic['leavestaken'] = k[0] - j[0]
        dic['leavebalance'] = float(p[0])- (k[0] - j[0])
        txn_list.append(dic)
        title = "Leave Balnace Report"
    return render_to_response('LeaveApp/LeaveBalance.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'username':username})
    
    