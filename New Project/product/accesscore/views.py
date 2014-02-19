# Create your views here.
import sys
from django.http import HttpResponse
from django.shortcuts import render_to_response,HttpResponseRedirect
from accesscore.models import *
from django.contrib.auth import authenticate, login
from django.db import connection
from django.contrib.sessions.models import Session
from forms import *
from django import forms
from django.conf import settings
from django.db.models import Avg, Max, Min, Count, Sum
from django.views.generic import list_detail # adding for testing 
from django.contrib import auth
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template.loader import get_template
from django.template import Context
from django.core.servers.basehttp import FileWrapper
import logging,datetime,os
from datetime import datetime,timedelta
from django.db.models import Q
from pprint import pprint
import os, mimetypes
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes


def CompanyDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    user = request.session['userid']
    Data = company.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = company.objects.get(id = Did)
        name = obj.name
        del request.session['id']
        msg = 'Company ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = company.objects.get(id = Newid)
        name = obj.name
        del request.session['txn.id']
        msg = 'Company ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = company.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Company Successfully Deleted'
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
        dic['Name'] = Data[i].name
        dic['code'] = Data[i].code
        dic['description'] = Data[i].description
        txn_list.append(dic)
    title = "Company List"
    return render_to_response('AccessCore/CompanyDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
def Edit_Company(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Edit_Company/'+id+'/'
    Cancel_url = '/AccessCore/Forms/CompanyDetails/'
    title = "Edit Company"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Company',status = 'Active')
    txnreport = company.objects.get(id = id)
    form = Companyform(instance=txnreport)
    if request.method == 'POST':
        form = Companyform(request.POST, instance=txnreport)
        if Companyform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save(commit = False)
            txn.modifiedbyuserid = user
            txn.save()
            print "AAAAAAAAA",request.POST.items()
            for i in columns:
                updating(request,i.field_type,request.POST[i.fieldname],txn.pk,i)
            return HttpResponseRedirect('/AccessCore/Forms/CompanyDetails')
    else:
        fordic(request,id)
        dic = fordic(request,id)
        print "SUMANTH",dic
        form = Companyform(instance=txnreport,initial = dic)    
    return render_to_response('AccessCore/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_Company(request,id):
    try:
        f = company.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/CompanyDetails') 
    except Exception:
        message = "Cannot Delete Company,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/CompanyDetails') 
def Add_Company(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Add_Company/'
    Cancel_url = '/AccessCore/Forms/CompanyDetails/'
    title = "Add Company"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Company',status = 'Active')
    if request.method == 'POST':
        form = Companyform(request.POST)
        print "SSSSSSSSS",request.POST.items()
        if form.is_valid():
            txn = form.save(commit = False)
            txn.createdbyuserid,txn.modifiedbyuserid = user,user
            txn.save()
            request.session['txn.id'] = txn.id
            for i in columns:
                b1 = com_feature_field_values(entityvalueid = txn.pk,feature_field=i).save()
                saving(request,i.field_type,request.POST[i.fieldname])
            return HttpResponseRedirect('/AccessCore/Forms/CompanyDetails')
    else:
        form = Companyform()
        print "SSSS",form.fields
    return render_to_response('AccessCore/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
##############    
def DepartmentDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Data = department.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = department.objects.get(id = Did)
        name = obj.name
        del request.session['id']
        msg = 'Department ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = department.objects.get(id = Newid)
        name = obj.name
        del request.session['txn.id']
        msg = 'Department ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = department.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Department Successfully Deleted'
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
        dic['company'] = Data[i].companyid
        dic['code'] = Data[i].code
        dic['description'] = Data[i].description
        txn_list.append(dic)
    title = "Departments List"
    return render_to_response('AccessCore/DepartmentDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
    
def Edit_Department(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Edit_Department/'+id+'/'
    Cancel_url = '/AccessCore/Forms/DepartmentDetails/'
    title = "Edit Department"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Department',status = 'Active')
    txnreport = department.objects.get(id = id)
    form = Departmentform(instance=txnreport)
    if request.method == 'POST':
        form = Departmentform(request.POST, instance=txnreport)
        if Departmentform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save(commit = False)
            txn.modifiedbyuserid = user
            txn.save()
            for i in columns:
                updating(request,i.field_type,request.POST[i.fieldname],txn.pk,i)
            return HttpResponseRedirect('/AccessCore/Forms/DepartmentDetails')
    else:
        fordic(request,id)
        dic = fordic(request,id)
        form = Departmentform(instance=txnreport,initial = dic)      
    return render_to_response('AccessCore/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_Department(request,id):
    try:
        f = department.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/DepartmentDetails')
    except Exception:
        message = "Cannot Delete Row,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/DepartmentDetails')
def Add_Department(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Add_Department/'
    Cancel_url = '/AccessCore/Forms/DepartmentDetails/'
    title = "Add Department"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Department',status = 'Active')
    if request.method == 'POST':
        form = Departmentform(request.POST)
        if form.is_valid():
            txn = form.save(commit = False)
            txn.createdbyuserid,txn.modifiedbyuserid = user,user
            txn.save()
            request.session['txn.id'] = txn.id
            for i in columns:
                b1 = com_feature_field_values(entityvalueid = txn.pk,feature_field=i).save()
                saving(request,i.field_type,request.POST[i.fieldname])
            return HttpResponseRedirect('/AccessCore/Forms/DepartmentDetails')
    else:
        form = Departmentform()
    return render_to_response('AccessCore/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
###########################################      
def PersonDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Data = person.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = person.objects.get(id = Did)
        name = obj.first_name
        del request.session['id']
        msg = 'Person ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = person.objects.get(id = Newid)
        name = obj.first_name
        del request.session['txn.id']
        msg = 'Person ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = person.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Person Successfully Deleted'
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
        dic['UserID'] = Data[i].personid
        dic['First_Name'] = Data[i].first_name
        dic['Last_Name'] = Data[i].last_name
        dic['Disp_Name'] = Data[i].disp_name
        dic['departmentid'] = Data[i].departmentid
        dic['person_type'] = Data[i].persontype
        dic['Gender'] = Data[i].gender
        dic['Address'] = Data[i].address
        dic['City'] = Data[i].city
        dic['Country'] = Data[i].country
        dic['Primary_Email'] = Data[i].primary_email
        dic['Secondary_Email'] = Data[i].secondary_email
        txn_list.append(dic)
    paginator = Paginator(txn_list,5)           
    title = "Persons List"
    return render_to_response('AccessCore/PersonDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,"msg":msg,'username':username})
def Edit_Person(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Edit_Person/'+id+'/'
    Cancel_url = '/AccessCore/Forms/PersonDetails/'
    title = "Edit Person"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Person',status = 'Active')
    txnreport = person.objects.get(id = id)
    try:
        accesschnge = accessor.objects.get(access_id = txnreport.personid)
    except Exception :
       b1=accessor(access_id=txnreport.personid, accessortype='Person')
       b1.save()
       accesschnge = accessor.objects.get(access_id = txnreport.personid)
    form = Personform(instance=txnreport)
    if request.method == 'POST':
       form = Personform(request.POST, instance=txnreport)
       UserID = request.POST["personid"]
       if Personform(instance=txnreport).has_changed():
           request.session['id'] = id
       if form.is_valid():
           txn = form.save(commit = False)
           txn.modifiedbyuserid = user
           txn.save()
           accesschnge.access_id = UserID
           accesschnge.save()
           for i in columns:
                updating(request,i.field_type,request.POST[i.fieldname],txn.pk,i)
           return HttpResponseRedirect('/AccessCore/Forms/PersonDetails')
    else:
        fordic(request,id)
        dic = fordic(request,id)
        form = Personform(instance=txnreport,initial = dic)      
    return render_to_response('AccessCore/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_Person(request,id):
    try:
        personobj = person.objects.get(id=id)
        request.session['deleteid'] = id
        accsrdel = accessor.objects.filter(access_id=personobj.userid).delete()
        f = person.objects.filter(id=id).delete()
        com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/PersonDetails')
    except Exception:
        message = "Cannot Delete Row,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/PersonDetails')
def Add_Person(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Add_Person/'
    Cancel_url = '/AccessCore/Forms/PersonDetails/'
    title = "Add Person"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Person',status = 'Active')
    if request.method == 'POST':
        form = Personform(request.POST)
        UserID = request.POST["personid"]
        if form.is_valid():
            txn = form.save(commit = False)
            txn.createdbyuserid,txn.modifiedbyuserid = user,user
            txn.save()
            b1=accessor(access_id=UserID, accessortype='Person')
            b1.save() 
            request.session['txn.id'] = txn.id
            for i in columns:
                b1 = com_feature_field_values(entityvalueid = txn.pk,feature_field=i).save()
                saving(request,i.field_type,request.POST[i.fieldname])
            return HttpResponseRedirect('/AccessCore/Forms/PersonDetails')
    else:
        form = Personform()
    return render_to_response('AccessCore/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
        
########################################  
def CardDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Data = card.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = card.objects.get(id = Did)
        name = obj.cardnumber
        del request.session['id']
        msg = 'Card ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = card.objects.get(id = Newid)
        name = obj.cardnumber
        del request.session['txn.id']
        msg = 'Card ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = card.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Card Successfully Deleted'
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
        dic['cardnumber'] = Data[i].cardnumber
        dic['startdate'] = Data[i].startdate
        dic['expirydate'] = Data[i].expirydate
        dic['pin'] = Data[i].pin
        dic['status'] = Data[i].status
        txn_list.append(dic)
    title = "Card List"
    return render_to_response('AccessCore/CardDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
def Edit_Card(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Edit_Card/'+id+'/'
    Cancel_url = '/AccessCore/Forms/CardDetails/'
    title = "Edit Card"
    txnreport = card.objects.get(id = id)
    columns = com_feature_fields.objects.filter(feature_table__table = 'Card',status = 'Active')
    form = Cardform(instance=txnreport)
    if request.method == 'POST':
        form = Cardform(request.POST, instance=txnreport)
        if Cardform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save(commit = False)
            txn.modifiedbyuserid = user
            txn.save()
            for i in columns:
                updating(request,i.field_type,request.POST[i.fieldname],txn.pk,i)
            return HttpResponseRedirect('/AccessCore/Forms/CardDetails')
    else:
        fordic(request,id)
        dic = fordic(request,id)
        form = Cardform(instance=txnreport,initial = dic)        
    return render_to_response('AccessCore/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_Card(request,id):
    try:
        f = card.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/CardDetails')
    except Exception:
        message = "Cannot Delete Row,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/CardDetails')
def Add_Card(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    columns = com_feature_fields.objects.filter(feature_table__table = 'Card',status = 'Active')
    if request.method == 'POST':
        form = Cardform(request.POST)
        if form.is_valid():
            txn = form.save(commit = False)
            txn.createdbyuserid,txn.modifiedbyuserid = user,user
            txn.save()
            request.session['txn.id'] = txn.id
            for i in columns:
                b1 = com_feature_field_values(entityvalueid = txn.pk,feature_field=i).save()
                saving(request,i.field_type,request.POST[i.fieldname])
            return HttpResponseRedirect('/AccessCore/Forms/CardDetails')
    else:
        form = Cardform()
    return render_to_response('AccessCore/Add_Card.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username})
############################################

def VehicleDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Data = vehicle.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = vehicle.objects.get(id = Did)
        name = obj.vehicle_number
        del request.session['id']
        msg = 'Vehicle ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = vehicle.objects.get(id = Newid)
        name = obj.vehicle_number
        del request.session['txn.id']
        msg = 'Vehicle ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = vehicle.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Vehicle Successfully Deleted'
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
        dic['vehicle_number'] = Data[i].vehicle_number
        dic['type'] = Data[i].type
        dic['departmentid'] = Data[i].departmentid
        dic['code'] = Data[i].code
        dic['description'] = Data[i].description   
        txn_list.append(dic)
    title = "Vehicle List"
    return render_to_response('AccessCore/VehicleDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
def Edit_Vehicle(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Edit_Vehicle/'+id+'/'
    Cancel_url = '/AccessCore/Forms/VehicleDetails/'
    title = "Edit Vehicle"
    txnreport = vehicle.objects.get(id = id)
    txn = com_feature_field_values.objects.filter(entityvalueid = id)
    columns = com_feature_fields.objects.filter(feature_table__table = 'Vehicle',status = 'Active')
    try:
       accesschnge = accessor.objects.get(access_id = txnreport.vehicle_number)
    except Exception :
       b1=accessor(access_id=txnreport.vehicle_number, AccessorType='Vehicle')
       b1.save()
       accesschnge = accessor.objects.get(access_id = txnreport.vehicle_number)
    form = Vehicleform(instance=txnreport)
    if request.method == 'POST':
        form = Vehicleform(request.POST, instance=txnreport)
        Vehiclenumber = request.POST["vehicle_number"]
        if Vehicleform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            obj = form.save(commit = False)
            obj.modifiedbyuserid = user
            obj.save()
            accesschnge.access_id = Vehiclenumber
            accesschnge.save()
            for i in columns:
                updating(request,i.field_type,request.POST[i.fieldname],obj.pk,i)
            return HttpResponseRedirect('/AccessCore/Forms/VehicleDetails')
    else:
        fordic(request,id)
        dic = fordic(request,id)
        form = Vehicleform(instance=txnreport,initial = dic)         
    return render_to_response('AccessCore/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_Vehicle(request,id):
    try:
        obj = vehicle.objects.get(id=id)
        accsrdel = accessor.objects.filter(access_id=obj.vehicle_number).delete()
        f = vehicle.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/VehicleDetails')
    except Exception:
        message = "Cannot Delete Row,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/VehicleDetails')
def Add_Vehicle(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Add_Vehicle/'
    Cancel_url = '/AccessCore/Forms/VehicleDetails/'
    title = "Add Vehicle"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Vehicle',status = 'Active')
    if request.method == 'POST':
        form = Vehicleform(request.POST)
        Vehiclenumber = request.POST["vehicle_number"]
        if form.is_valid():
            obj = form.save(commit = False)
            obj.createdbyuserid,obj.modifiedbyuserid = user,user
            obj.save()
            b1=accessor(access_id=Vehiclenumber, accessortype='Vehicle')
            b1.save() 
            request.session['txn.id'] = obj.id
            for i in columns:
                b1 = com_feature_field_values(entityvalueid = obj.pk,feature_field=i).save()
                saving(request,i.field_type,request.POST[i.fieldname])
            return HttpResponseRedirect('/AccessCore/Forms/VehicleDetails')
    else:
        form = Vehicleform()    
    return render_to_response('AccessCore/Add_Details.html',{'form':form,'columns':columns,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
    
 ###########################
def saving(request,value,a):
    if value == 1:
        obj = com_feature_field_values.objects.latest('id')
        obj.Stringvalue = a
        obj.save()     
    if value == 2:
        obj = com_feature_field_values.objects.latest('id')      
        if a!= '':
            obj.Integergvalue = a
        else:
            obj.Integergvalue = 0
        obj.save()     
    if value == 3:
        obj = com_feature_field_values.objects.latest('id')
        obj.Booleanvalue = a
        obj.save()     
    if value == 4:
        obj = com_feature_field_values.objects.latest('id')
        if a!= '':
            obj.Doublevalue = a
        else:
            obj.Doublevalue = 0.0
        obj.save()     
    if value == 5:
        obj = com_feature_field_values.objects.latest('id')
        obj.DateTimevalue = a
        obj.save()     
    if value == 6:
        obj = com_feature_field_values.objects.latest('id')
        if a!= '':
            val = com_list.objects.get(id = a)
            obj.Listvalue = val.dropdownvalue
        else:
            obj.Listvalue = 'NULL'
        obj.save() 
    
def updating(request,value,a,b,c):
    obj = com_feature_field_values.objects.filter(entityvalueid = b,feature_field=c)
    if value == 1:
        if not obj:
            com_feature_field_values(entityvalueid = b,feature_field=c,Stringvalue=a).save()
        else:
            com_feature_field_values.objects.filter(entityvalueid = b,feature_field=c).update(Stringvalue=a)
    if value == 2:
        if not obj:
            if a!= '':
                com_feature_field_values(entityvalueid = b,feature_field=c,Integergvalue=a).save()
            else:
                com_feature_field_values(entityvalueid = b,feature_field=c,Integergvalue=0).save()
        elif a!= '':
            obj.update(Integergvalue = a)
        else:
            obj.update(Integergvalue = 0)
    if value == 3:
        if not obj:
            com_feature_field_values(entityvalueid = b,feature_field=c,Booleanvalue=a).save()
        else:
            com_feature_field_values.objects.filter(entityvalueid = b,feature_field=c).update(Booleanvalue=a)
    if value == 4:
        if not obj:
            if a!= '':
                com_feature_field_values(entityvalueid = b,feature_field=c,Doublevalue=a).save()
            else:
                com_feature_field_values(entityvalueid = b,feature_field=c,Doublevalue=0.0).save()
        elif a!= '':
            obj.update(Doublevalue = a)
        else:
            obj.update(Doublevalue = 0.0)
    if value == 5:
        if not obj:
            com_feature_field_values(entityvalueid = b,feature_field=c,DateTimevalue=a).save()
        else:
            com_feature_field_values.objects.filter(entityvalueid = b,feature_field=c).update(DateTimevalue=a)
    if value == 6:
        if not obj:
            if a!= '':
                com_feature_field_values(entityvalueid = b,feature_field=c,Listvalue=a).save()
            else:
                com_feature_field_values(entityvalueid = b,feature_field=c,Listvalue='NULL').save()
        elif a!= '':
            val = com_list.objects.get(id = a)
            obj.update(Listvalue = val.dropdownvalue)
        else:
            obj.update(Listvalue = 'NULL')
            
            
def fordic(request,id):
    b = [field.name for field in com_feature_field_values._meta.fields]
    qs_new = com_feature_field_values.objects.filter(entityvalueid = id).values(*b)
    dic = {}
    for i in qs_new:
        for b in i:
            if i[b] is not None and b not in ('entityvalueid','feature_field','id'):
                z = com_feature_fields.objects.get(id = i['feature_field'])             
                dic[z.fieldname] = i[b]
    return dic
        
#######################################
        
def DeviceDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Data = device.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = device.objects.get(id = Did)
        name = obj.name
        del request.session['id']
        msg = 'Device ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = device.objects.get(id = Newid)
        name = obj.name
        del request.session['txn.id']
        msg = 'Device ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = device.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Device Successfully Deleted'
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
        dic['macaddress'] = Data[i].macaddress
        dic['ipaddress'] = Data[i].ipaddress
        dic['hostname'] = Data[i].hostname
        dic['devicetype'] = Data[i].devicetype   
        dic['departmentid'] = Data[i].departmentid   
        txn_list.append(dic)
    title = "Device List"
    return render_to_response('AccessCore/DeviceDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
def Edit_Device(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Edit_Device/'+id+'/'
    Cancel_url = '/AccessCore/Forms/DeviceDetails/'
    title = "Edit Device"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Device',status = 'Active')
    txnreport = device.objects.get(id = id)
    form = Deviceform(instance=txnreport)
    if request.method == 'POST':
        form = Deviceform(request.POST, instance=txnreport)
        if Deviceform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save(commit = False)
            txn.modifiedbyuserid = user
            txn.save()
            for i in columns:
                updating(request,i.field_type,request.POST[i.fieldname],txn.pk,i)
            return HttpResponseRedirect('/AccessCore/Forms/DeviceDetails')
    else:
        fordic(request,id)
        dic = fordic(request,id)
        form = Deviceform(instance=txnreport,initial = dic)  
    return render_to_response('AccessCore/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_Device(request,id):
    try:
        f = device.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/DeviceDetails')
    except Exception:
        message = "Cannot Delete Row,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/DeviceDetails')
def Add_Device(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Add_Device/'
    Cancel_url = '/AccessCore/Forms/DeviceDetails/'
    title = "Add Device"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Device',status = 'Active')
    if request.method == 'POST':
        form = Deviceform(request.POST)
        if form.is_valid():
            txn = form.save(commit = False)
            txn.createdbyuserid,txn.modifiedbyuserid = user,user
            txn.save()
            request.session['txn.id'] = txn.id
            for i in columns:
                b1 = com_feature_field_values(entityvalueid = txn.pk,feature_field=i).save()
                saving(request,i.field_type,request.POST[i.fieldname])
            return HttpResponseRedirect('/AccessCore/Forms/DeviceDetails')
    else:
        form = Deviceform()
    return render_to_response('AccessCore/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
###################################
    
def PersonTypeDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Data = person_type.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = person_type.objects.get(id = Did)
        name = obj.name
        del request.session['id']
        msg = 'Person_Type ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = person_type.objects.get(id = Newid)
        name = obj.name
        del request.session['txn.id']
        msg = 'Person_Type ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = person_type.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Person_Type Successfully Deleted'
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
    title = "PersonType List"
    return render_to_response('AccessCore/PersonTypeDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
def Edit_PersonType(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Edit_PersonType/'+id+'/'
    Cancel_url = '/AccessCore/Forms/PersonTypeDetails/'
    title = "Edit PersonType"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Person_Type',status = 'Active')
    txnreport = person_type.objects.get(id = id)
    form = Person_Typeform(instance=txnreport)
    if request.method == 'POST':
        form = Person_Typeform(request.POST, instance=txnreport)
        if Person_Typeform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save(commit = False)
            txn.modifiedbyuserid = user
            txn.save()
            for i in columns:
                updating(request,i.field_type,request.POST[i.fieldname],txn.pk,i)
            return HttpResponseRedirect('/AccessCore/Forms/PersonTypeDetails')
    else:
        fordic(request,id)
        dic = fordic(request,id)
        form = Person_Typeform(instance=txnreport,initial = dic)  
    return render_to_response('AccessCore/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_PersonType(request,id):
    try:
        f = person_type.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/PersonTypeDetails')
    except Exception:
        message = "Cannot Delete Row,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/PersonTypeDetails')
def Add_PersonType(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Add_PersonType/'
    Cancel_url = '/AccessCore/Forms/PersonTypeDetails/'
    title = "Add PersonType"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Person_Type',status = 'Active')
    if request.method == 'POST':
        form = Person_Typeform(request.POST)
        if form.is_valid():
            txn = form.save(commit = False)
            txn.createdbyuserid,txn.modifiedbyuserid = user,user
            txn.save()
            request.session['txn.id'] = txn.id
            for i in columns:
                b1 = com_feature_field_values(entityvalueid = txn.pk,feature_field=i).save()
                saving(request,i.field_type,request.POST[i.fieldname])
            return HttpResponseRedirect('/AccessCore/Forms/PersonTypeDetails')
    else:
        form = Person_Typeform()
    return render_to_response('AccessCore/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
#####################
    
def VehicleTypeDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Data = vehicle_type.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = vehicle_type.objects.get(id = Did)
        name = obj.name
        del request.session['id']
        msg = 'Vehicle_Type ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = vehicle_type.objects.get(id = Newid)
        name = obj.name
        del request.session['txn.id']
        msg = 'Vehicle_Type ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = vehicle_type.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Vehicle_Type Successfully Deleted'
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
    title = "VehicleType List"
    return render_to_response('AccessCore/VehicleTypeDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
def Edit_VehicleType(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Edit_VehicleType/'+id+'/'
    Cancel_url = '/AccessCore/Forms/VehicleTypeDetails/'
    title = "Edit VehicleType"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Vehicle_Type',status = 'Active')
    txnreport = vehicle_type.objects.get(id = id)
    form = Vehicle_Typeform(instance=txnreport)
    if request.method == 'POST':
        form = Vehicle_Typeform(request.POST, instance=txnreport)
        if Vehicle_Typeform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save(commit = False)
            txn.modifiedbyuserid = user
            txn.save()
            for i in columns:
                updating(request,i.field_type,request.POST[i.fieldname],txn.pk,i)
            return HttpResponseRedirect('/AccessCore/Forms/VehicleTypeDetails')
    else:
        fordic(request,id)
        dic = fordic(request,id)
        form = Vehicle_Typeform(instance=txnreport,initial = dic)  
    return render_to_response('AccessCore/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_VehicleType(request,id):
    try:
        f = vehicle_type.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/VehicleTypeDetails')
    except Exception:
        message = "Cannot Delete Row,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/VehicleTypeDetails')
def Add_VehicleType(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Add_VehicleType/'
    Cancel_url = '/AccessCore/Forms/VehicleTypeDetails/'
    title = "Add VehicleType"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Vehicle_Type',status = 'Active')
    if request.method == 'POST':
        form = Vehicle_Typeform(request.POST)
        if form.is_valid():
            txn = form.save(commit = False)
            txn.createdbyuserid,txn.modifiedbyuserid = user,user
            txn.save()
            request.session['txn.id'] = txn.id
            for i in columns:
                b1 = com_feature_field_values(entityvalueid = txn.pk,feature_field=i).save()
                saving(request,i.field_type,request.POST[i.fieldname])
            return HttpResponseRedirect('/AccessCore/Forms/VehicleTypeDetails')
    else:
        form = Vehicle_Typeform()
    return render_to_response('AccessCore/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
    
###############################################

def DeviceGroupDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Data = devicegroup.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = devicegroup.objects.get(id = Did)
        name = obj.name
        del request.session['id']
        msg = 'Devicegroup ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = devicegroup.objects.get(id = Newid)
        name = obj.name
        del request.session['txn.id']
        msg = 'Devicegroup ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = devicegroup.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Devicegroup Successfully Deleted'
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
        dic['deviceid'] = Data[i].deviceid.all()
        txn_list.append(dic)
    title = "DeviceGroup List"
    return render_to_response('AccessCore/DeviceGroupDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'msg':msg,'username':username,'title':title})
def Edit_DeviceGroup(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Edit_DeviceGroup/'+id+'/'
    Cancel_url = '/AccessCore/Forms/DeviceGroupDetails/'
    title = "Edit DeviceGroup"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Devicegroup',status = 'Active')
    txnreport = devicegroup.objects.get(id = id)
    form = DeviceGroupform(instance=txnreport)
    if request.method == 'POST':
        form = DeviceGroupform(request.POST, instance=txnreport)
        if DeviceGroupform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save()
            txn.modifiedbyuserid = user
            txn.save()
            for i in columns:
                updating(request,i.field_type,request.POST[i.fieldname],txn.pk,i)
            return HttpResponseRedirect('/AccessCore/Forms/DeviceGroupDetails')
    else:
        fordic(request,id)
        dic = fordic(request,id)
        form = DeviceGroupform(instance=txnreport,initial = dic)  
    return render_to_response('AccessCore/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_DeviceGroup(request,id):
    try:
        f = devicegroup.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/DeviceGroupDetails')
    except Exception:
        message = "Cannot Delete Row,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/DeviceGroupDetails')
def Add_DeviceGroup(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Add_DeviceGroup/'
    Cancel_url = '/AccessCore/Forms/DeviceGroupDetails/'
    title = "Add DeviceGroup"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Devicegroup',status = 'Active')
    if request.method == 'POST':
        form = DeviceGroupform(request.POST)
        if form.is_valid():
            txn = form.save()
            txn.createdbyuserid,txn.modifiedbyuserid = user,user
            txn.save()
            request.session['txn.id'] = txn.id
            for i in columns:
                b1 = com_feature_field_values(entityvalueid = txn.pk,feature_field=i).save()
                saving(request,i.field_type,request.POST[i.fieldname])
            return HttpResponseRedirect('/AccessCore/Forms/DeviceGroupDetails')
    else:
        form = DeviceGroupform()
    return render_to_response('AccessCore/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})

###########################################
 
def ScheduleDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Data = schedule.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = schedule.objects.get(id = Did)
        name = obj.name
        del request.session['id']
        msg = 'Schedule ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = schedule.objects.get(id = Newid)
        name = obj.name
        del request.session['txn.id']
        msg = 'Schedule ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = schedule.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Schedule Successfully Deleted'
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
        dic['starttime'] = Data[i].starttime
        dic['endtime'] = Data[i].endtime     
        txn_list.append(dic)
    title = "Schedule List"
    return render_to_response('AccessCore/SheduleDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
def Edit_Schedule(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Edit_Schedule/'+id+'/'
    Cancel_url = '/AccessCore/Forms/ScheduleDetails/'
    title = "Edit Schedule"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Schedule',status = 'Active')
    txnreport = schedule.objects.get(id = id)
    form = Scheduleform(instance=txnreport)
    if request.method == 'POST':
        form = Scheduleform(request.POST, instance=txnreport)
        if Scheduleform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save(commit = False)
            txn.modifiedbyuserid = user
            txn.save()
            for i in columns:
                updating(request,i.field_type,request.POST[i.fieldname],txn.pk,i)
            return HttpResponseRedirect('/AccessCore/Forms/ScheduleDetails')
    else:
        fordic(request,id)
        dic = fordic(request,id)
        form = Scheduleform(instance=txnreport,initial = dic)  
    return render_to_response('AccessCore/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_Schedule(request,id):
    try:
        f = schedule.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/ScheduleDetails')
    except Exception:
        message = "Cannot Delete Row,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/ScheduleDetails')
def Add_Schedule(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Add_Schedule/'
    Cancel_url = '/AccessCore/Forms/ScheduleDetails/'
    title = "Add Schedule"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Schedule',status = 'Active')
    if request.method == 'POST':
        form = Scheduleform(request.POST)
        if form.is_valid():
            txn = form.save(commit = False)
            txn.createdbyuserid,txn.modifiedbyuserid = user,user
            txn.save()
            request.session['txn.id'] = txn.id
            for i in columns:
                b1 = com_feature_field_values(entityvalueid = txn.pk,feature_field=i).save()
                saving(request,i.field_type,request.POST[i.fieldname])
            return HttpResponseRedirect('/AccessCore/Forms/ScheduleDetails')
    else:
        form = Scheduleform()
    return render_to_response('AccessCore/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})

##############################################################

def AccessGroupDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Data = accessgroup.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = accessgroup.objects.get(id = Did)
        name = obj.name
        del request.session['id']
        msg = 'Accessgroup ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = accessgroup.objects.get(id = Newid)
        name = obj.name
        del request.session['txn.id']
        msg = 'Accessgroup ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = accessgroup.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Accessgroup Successfully Deleted'
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
        dic['devicegroup'] = Data[i].devicegroup
        dic['scheduleid'] = Data[i].scheduleid     
        txn_list.append(dic)
    title = "Access Group List"
    return render_to_response('AccessCore/AccessGroupDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
def Edit_AccessGroup(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Edit_AccessGroup/'+id+'/'
    Cancel_url = '/AccessCore/Forms/AccessGroupDetails/'
    title = "Edit AccessGroup"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Accessgroup',status = 'Active')
    txnreport = accessgroup.objects.get(id = id)
    form = Accessgroupform(instance=txnreport)
    if request.method == 'POST':
        form = Accessgroupform(request.POST, instance=txnreport)
        if Accessgroupform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save(commit = False)
            txn.modifiedbyuserid = user
            txn.save()
            for i in columns:
                updating(request,i.field_type,request.POST[i.fieldname],txn.pk,i)
            return HttpResponseRedirect('/AccessCore/Forms/AccessGroupDetails')
    else:
        fordic(request,id)
        dic = fordic(request,id)
        form = Accessgroupform(instance=txnreport,initial = dic)  
    return render_to_response('AccessCore/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_AccessGroup(request,id):
    try:
        f = accessgroup.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/AccessGroupDetails')
    except Exception:
        message = "Cannot Delete Row,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/AccessGroupDetails')
def Add_AccessGroup(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Add_AccessGroup/'
    Cancel_url = '/AccessCore/Forms/AccessGroupDetails/'
    title = "Add AccessGroup"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Accessgroup',status = 'Active')
    if request.method == 'POST':
        form = Accessgroupform(request.POST)
        if form.is_valid():
            txn = form.save(commit = False)
            txn.createdbyuserid,txn.modifiedbyuserid = user,user
            txn.save()
            request.session['txn.id'] = txn.id
            for i in columns:
                b1 = com_feature_field_values(entityvalueid = txn.pk,feature_field=i).save()
                saving(request,i.field_type,request.POST[i.fieldname])
            return HttpResponseRedirect('/AccessCore/Forms/AccessGroupDetails')
    else:
        form = Accessgroupform()
    return render_to_response('AccessCore/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})

############################################

def AccessGroupAssignedtoCardDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Data = accessgroupassigntocard.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = accessgroupassigntocard.objects.get(id = Did)
        name = obj.cardid
        del request.session['id']
        msg = 'Accessgroupassigntocard ' +str(name)+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = accessgroupassigntocard.objects.get(id = Newid)
        name = obj.cardid
        del request.session['txn.id']
        msg = 'Accessgroupassigntocard ' +str(name)+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = accessgroupassigntocard.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Accessgroupassigntocard Successfully Deleted'
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
        dic['cardid'] = Data[i].cardid
        dic['departmentid'] = Data[i].departmentid     
        dic['accessgroupid'] = Data[i].accessgroupid     
        txn_list.append(dic)
    title = "Access Group Assigned to card List"
    return render_to_response('AccessCore/AccessGroupAssignedtoCardDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
def Edit_AccessGroupAssignedtoCard(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Edit_AccessGroupAssignedtoCard/'+id+'/'
    Cancel_url = '/AccessCore/Forms/AccessGroupAssignedtoCardDetails/'
    title = "Edit AccessGroupAssignedtoCard"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Accessgroupassigntocard',status = 'Active')
    txnreport = accessgroupassigntocard.objects.get(id = id)
    form = Accessgroupassigntocardform(instance=txnreport)
    if request.method == 'POST':
        form = Accessgroupassigntocardform(request.POST, instance=txnreport)
        if Accessgroupassigntocardform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save(commit = False)
            txn.modifiedbyuserid = user
            txn.save()
            for i in columns:
                updating(request,i.field_type,request.POST[i.fieldname],txn.pk,i)
            return HttpResponseRedirect('/AccessCore/Forms/AccessGroupAssignedtoCardDetails')
    else:
        fordic(request,id)
        dic = fordic(request,id)
        form = Accessgroupassigntocardform(instance=txnreport,initial = dic)  
    return render_to_response('AccessCore/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_AccessGroupAssignedtoCard(request,id):
    try:
        f = accessgroupassigntocard.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/AccessGroupAssignedtoCardDetails')
    except Exception:
        message = "Cannot Delete Row,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/AccessGroupAssignedtoCardDetails')
def Add_AccessGroupAssignedtoCard(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Add_AccessGroupAssignedtoCard/'
    Cancel_url = '/AccessCore/Forms/AccessGroupAssignedtoCardDetails/'
    title = "Add AccessGroupAssignedtoCard"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Accessgroupassigntocard',status = 'Active')
    if request.method == 'POST':
        form = Accessgroupassigntocardform(request.POST)
        if form.is_valid():
            txn = form.save(commit = False)
            txn.createdbyuserid,txn.modifiedbyuserid = user,user
            txn.save()
            request.session['txn.id'] = txn.id
            for i in columns:
                b1 = com_feature_field_values(entityvalueid = txn.pk,feature_field=i).save()
                saving(request,i.field_type,request.POST[i.fieldname])
            return HttpResponseRedirect('/AccessCore/Forms/AccessGroupAssignedtoCardDetails')
    else:
        form = Accessgroupassigntocardform()
    return render_to_response('AccessCore/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
############################################

def CardAccessorDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Data = card_to_accessor_map.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = card_to_accessor_map.objects.get(id = Did)
        name = obj.card
        del request.session['id']
        msg = 'Card_To_Accessor_Map '+str(name)+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = card_to_accessor_map.objects.get(id = Newid)
        name = obj.card
        del request.session['txn.id']
        msg = 'Card Accessor '+str(name)+'  Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = card_to_accessor_map.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Card Accessor Successfully Deleted'
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
        dic['card'] = Data[i].card
        dic['accessor'] = Data[i].accessor.all()   
        txn_list.append(dic)
    title = "Card accessor List"
    return render_to_response('AccessCore/CardAccessorDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
def Edit_CardAccessor(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Edit_CardAccessor/'+id+'/'
    Cancel_url = '/AccessCore/Forms/CardAccessorDetails/'
    title = "Edit CardAccessor"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Card_To_Accessor_Map',status = 'Active')
    txnreport = card_to_accessor_map.objects.get(id = id)
    form = CardtoAccessorform(instance=txnreport)
    if request.method == 'POST':
        form = CardtoAccessorform(request.POST, instance=txnreport)
        if CardtoAccessorform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save()
            txn.modifiedbyuserid = user
            txn.save()
            for i in columns:
                updating(request,i.field_type,request.POST[i.fieldname],txn.pk,i)
            return HttpResponseRedirect('/AccessCore/Forms/CardAccessorDetails')
    else:
        fordic(request,id)
        dic = fordic(request,id)
        form = CardtoAccessorform(instance=txnreport,initial = dic)  
    return render_to_response('AccessCore/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_CardAccessor(request,id):
    try:
        f = card_to_accessor_map.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/CardAccessorDetails')
    except Exception:
        message = "Cannot Delete Row,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/CardAccessorDetails')
def Add_CardAccessor(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Add_CardAccessor/'
    Cancel_url = '/AccessCore/Forms/CardAccessorDetails/'
    title = "Add CardAccessor"
    columns = com_feature_fields.objects.filter(feature_table__table = 'Card_To_Accessor_Map',status = 'Active')
    if request.method == 'POST':
        form = CardtoAccessorform(request.POST)
        if form.is_valid():
            txn = form.save()
            txn.createdbyuserid,txn.modifiedbyuserid = user,user
            txn.save()
            request.session['txn.id'] = txn.id
            for i in columns:
                b1 = com_feature_field_values(entityvalueid = txn.pk,feature_field=i).save()
                saving(request,i.field_type,request.POST[i.fieldname])
            return HttpResponseRedirect('/AccessCore/Forms/CardAccessorDetails')
    else:
        form = CardtoAccessorform()
    return render_to_response('AccessCore/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
    
def FeatureForm(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Data = com_feature_fields.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = com_feature_fields.objects.get(id = Did)
        name = obj.fieldname
        del request.session['id']
        msg = 'Feature Column '+str(name)+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = com_feature_fields.objects.get(id = Newid)
        name = obj.fieldname
        del request.session['txn.id']
        msg = 'Feature Column '+str(name)+'  Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = com_feature_fields.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Feature Column Successfully Deleted'
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
        dic['fieldname'] = Data[i].fieldname
        dic['field_type'] = Data[i].field_type  
        dic['feature_table'] = Data[i].feature_table  
        dic['status'] = Data[i].status
        txn_list.append(dic)
    title = "Feature Columns List"
    return render_to_response('AccessCore/FeatureFormDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
    
def Edit_Feature_Form(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Edit_Feature_Form/'+id+'/'
    Cancel_url = '/AccessCore/Forms/Feature_Form/'
    title = "Edit Feature Form"
    txnreport = com_feature_fields.objects.get(id = id)
    form = Fieldsform(instance=txnreport)
    if request.method == 'POST':
        form = Fieldsform(request.POST, instance=txnreport)
        if Fieldsform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save(commit = False)
            txn.modifiedbyuserid = user
            txn.save()
            return HttpResponseRedirect('/AccessCore/Forms/Feature_Form')
    else:
        form = Fieldsform(instance=txnreport)  
    return render_to_response('AccessCore/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_Feature_Form(request,id):
    try:
        f = com_feature_fields.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        # com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/Feature_Form')
    except Exception:
        message = "Cannot Delete Row,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/Feature_Form')
def Add_Feature_Form(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Add_Feature_Form/'
    Cancel_url = '/AccessCore/Forms/Feature_Form/'
    title = "Add Feature Form"
    if request.method == 'POST':
        form = Fieldsform(request.POST)
        if form.is_valid():
            txn = form.save(commit = False)
            txn.createdbyuserid,txn.modifiedbyuserid = user,user
            txn.save()
            request.session['txn.id'] = txn.id
            return HttpResponseRedirect('/AccessCore/Forms/Feature_Form')
    else:
        form = Fieldsform()
    return render_to_response('AccessCore/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
    
def ListDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Data = com_list.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = com_list.objects.get(id = Did)
        name = obj.fieldname
        del request.session['id']
        msg = 'Feature List '+str(name)+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = com_list.objects.get(id = Newid)
        name = obj.fieldname
        del request.session['txn.id']
        msg = 'Feature List '+str(name)+'  Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = com_list.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Feature List Successfully Deleted'
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
        dic['feature_field'] = Data[i].feature_field
        dic['dropdownvalue'] = Data[i].dropdownvalue  
        # dic['feature_table'] = Data[i].feature_table  
        txn_list.append(dic)
    title = "Feature List"
    return render_to_response('AccessCore/ListDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,'msg':msg,'username':username})
    
def Edit_ListDetails(request,id):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Edit_ListDetails/'+id+'/'
    Cancel_url = '/AccessCore/Forms/ListDetails/'
    title = "Edit Feature Form"
    txnreport = com_list.objects.get(id = id)
    form = Listform(instance=txnreport)
    if request.method == 'POST':
        form = Listform(request.POST, instance=txnreport)
        if Listform(instance=txnreport).has_changed():
            request.session['id'] = id
        if form.is_valid():
            txn = form.save(commit = False)
            txn.modifiedbyuserid = user
            txn.save()
            return HttpResponseRedirect('/AccessCore/Forms/ListDetails')
    else:
        form = Listform(instance=txnreport)  
    return render_to_response('AccessCore/Edit_Details.html',{'form':form,'order':id,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
def Delete_ListDetails(request,id):
    try:
        f = com_list.objects.filter(id=id).delete()
        request.session['deleteid'] = id
        # com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/ListDetails')
    except Exception:
        message = "Cannot Delete Row,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/ListDetails')
def Add_ListDetails(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    user = request.session['userid']
    username = request.session['username']
    Action_url = '/AccessCore/Forms/Add_ListDetails/'
    Cancel_url = '/AccessCore/Forms/ListDetails/'
    title = "Add Feature Form"
    if request.method == 'POST':
        form = Listform(request.POST)
        if form.is_valid():
            txn = form.save(commit = False)
            txn.createdbyuserid,txn.modifiedbyuserid = user,user
            txn.save()
            request.session['txn.id'] = txn.id
            return HttpResponseRedirect('/AccessCore/Forms/ListDetails')
    else:
        form = Listform()
    return render_to_response('AccessCore/Add_Details.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'username':username,'Action_url':Action_url,'Cancel_url':Cancel_url,'title':title})
    
def scan(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    try:
        cardtype1 = ATRCardType( toBytes( "3B 8F 80 01 80 4F 0C A0 00 00 03 06 0A 00 18 00 00 00 00 7A" ) )
        cardrequest = CardRequest( timeout=1, cardType=cardtype1)
        cardservice = cardrequest.waitforcard()
    except Exception:
       return render_to_response('AccessCore/Message.html',{'Rolefetures':rolefeatures,'projectname':pname,'msg':'Card not found','link':'admin_home'})
    cardservice.connection.connect()
    SELECT = [0xFF, 0xCA, 0x00, 0x00, 0x00]
    apdu = SELECT    
    response, sw1, sw2 = cardservice.connection.transmit( apdu )
    cardno = toHexString(response).replace(' ','')
    import simplejson
    data = []
    data.append({"msg": str(cardno)})
    json = simplejson.dumps(data)
    return HttpResponse(json,mimetype='application/json')
    # return HttpResponce(cardno)
    # return render_to_response('AccessCore/Add_Card.html',{'form':form,'Rolefetures':rolefeatures,'projectname':pname,'cardno':cardno})
    
#############################################

def PersonInfo(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    txn_list = []
    # try:
    for p in accessgroupassigntocard.objects.raw('select AGAC.id,PER.personid,First_Name fname,AC.cardnumber number,DEPT.name  Dname,DG.name DGname,SC.name Schedule,AG.name AGname from AccessCore_accessgroupassigntocard AGAC\
        inner join AccessCore_accessgroup AG on AGAC.accessgroupid_id = AG.id\
        inner join AccessCore_devicegroup DG on AG.devicegroup_id = DG.id\
        inner join AccessCore_schedule SC on AG.scheduleid_id = SC.id\
        inner join AccessCore_card AC on AGAC.cardid_id = AC.id\
        inner join AccessCore_card_to_accessor_map CTAM on AGAC.cardid_id = CTAM.card_id\
        inner join AccessCore_card_to_accessor_map_accessor CTAMA on CTAM.id = CTAMA.card_to_accessor_map_id\
        inner join AccessCore_accessor ACC on CTAMA.accessor_id = ACC.id\
        inner join AccessCore_person PER on ACC.access_id = PER.personid\
        inner join AccessCore_department DEPT on AGAC.departmentid_id = DEPT.id'):
        dic = {}
        dic['cardnumber'] = p.number
        dic['fname'] = p.fname    
        dic['dname'] = p.Dname
        dic['Gname'] = p.DGname
        Data = devicegroup.objects.get(name = p.DGname)
        dic1 = {}
        dic1['deviceid'] = Data.deviceid.all()
        dic['DGname'] = dic1['deviceid']
        dic['Schedule'] = p.Schedule
        dic['AGname'] = p.AGname
        txn_list.append(dic)
    title = "Person Details"
    table_headings = ['Cardnumber','Name','Department','Device Group Name','Device Group','Schedule','Accessor Group']
    url = "uam/home"
    columnfilters = [{'type':"text"} for i in table_headings]
    return render_to_response('AccessCore/PersonInfo.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'headings':table_headings,'title':title,'url':url,'columnfilters':columnfilters,'username':username})
    # except Exception:
        # return render_to_response('AccessCore/user_response.html',{"Rolefetures":rolefeatures,"projectname":pname,"msg":'No Records Found', "link":'uam/home','username':username})

def Reports_movement_today(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    try:
        txn_list = []
        from1 = str(datetime.now())[0:10]+ ' 00:00:00'
        to = str(datetime.now())[0:10]+ ' 23:59:59'
        for p in movement.objects.raw('select * from todaymovment where date between \'%s\' and \'%s\' order by id'%(from1,to)):
            dic = {}
            dic[1] = p.id
            dic[2] = p.access_id    
            dic[3] = p.accessortype    
            dic[4] = p.status    
            dic[5] = p.uid    
            dic[6] = p.name    
            dic[7] = p.AccessorName 
            dic[8] = p.date
            txn_list.append(dic)
        title = "Movement Report on "+str(datetime.now())[0:10]
        table_headings = ['ID','Accessor Code','Accessor Type','Status','UID','Access@','Accessor Name','Date & Time']
        columnfilters = [{'type':"text"} for i in table_headings]
        url = "uam/home"
        return render_to_response('AccessCore/Reports_movement_today.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'headings':table_headings,'title':title,'url':url,'columnfilters':columnfilters,'username':username})
    except Exception:
        return render_to_response('AccessCore/user_response.html',{"Rolefetures":rolefeatures,"projectname":pname,"msg":'No Records Found', "link":'uam/home','username':username})
def Reports_CustomReport(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    title = "Custom Movement Report"
    url = "AccessCore/Reports/CustomReport_Fun"
    return render_to_response('AccessCore/Range.html',{'Rolefetures':rolefeatures,'projectname':pname,'title':title,'url':url,'username':username})
    
def Reports_CustomReport_Fun(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    try:
        txn_list = []
        from1 = str(request.POST['from'])[0:16]+':00'
        to = str(request.POST['to'])[0:16]+':00'
        for p in movement.objects.raw('select * from todaymovment where date between \'%s\' and \'%s\' order by id'%(from1,to)):
            dic = {}
            dic[1] = p.id
            dic[2] = p.access_id    
            dic[3] = p.accessortype    
            dic[4] = p.status    
            dic[5] = p.uis    
            dic[6] = p.name    
            dic[7] = p.accessorname
            dic[8] = p.date
            txn_list.append(dic)
        title = "Custom Report Between "+from1+" and "+to
        table_headings = ['ID','Accessor Code','Accessor Type','Status','UID','Access@','Accessor Name','Date & Time']
        columnfilters = [{'type':"text"} for i in table_headings]
        url = "AccessCore/Reports/CustomReport"
        return render_to_response('AccessCore/Reports_movement_today.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'headings':table_headings,'title':title,'url':url,'columnfilters':columnfilters,'username':username})
    except Exception:
        return render_to_response('AccessCore/user_response.html',{"Rolefetures":rolefeatures,"projectname":pname,"msg":'No Records Found', "link":'AccessCore/Reports/CustomReport','username':username})
        
def Blockwise_Report(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Blocks = department.objects.all()
    title = "Blockwise Movement Report"
    url = "AccessCore/Reports/Blockwise_Report_Fun"
    return render_to_response('AccessCore/Range.html',{'Rolefetures':rolefeatures,'projectname':pname,'title':title,'url':url,'Blocks':Blocks,'username':username})
    
def Blockwise_Report_Fun(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    try:
        txn_list = []
        from1 = str(request.POST['from'])[0:16]+':00'
        to = str(request.POST['to'])[0:16]+':00'
        Block = request.POST['Blocks']
        for p in movement.objects.raw('select TM.* from todaymovment TM \
        left join AccessCore_department DEPT on DEPT.id = TM.departmentid_id where TM.date between \'%s\' and \'%s\' and DEPT.name = \'%s\' order by TM.id'%(from1,to,Block)):
            dic = {}
            dic[1] = p.id
            dic[2] = p.access_id    
            dic[3] = p.accessortype    
            dic[4] = p.status    
            dic[5] = p.uid    
            dic[6] = p.name    
            dic[7] = p.AccessorName 
            dic[8] = p.date
            txn_list.append(dic)
        title = str(Block)+" Report"
        table_headings = ['ID','Accessor Code','Accessor Type','Status','UID','Access@','Accessor Name','Date & Time']
        columnfilters = [{'type':"text"} for i in table_headings]
        url = "AccessCore/Reports/Blockwise_Report"
        return render_to_response('AccessCore/Reports_movement_today.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'headings':table_headings,'title':title,'url':url,'columnfilters':columnfilters,'username':username})
    except Exception:
        return render_to_response('AccessCore/user_response.html',{"Rolefetures":rolefeatures,"projectname":pname,"msg":'No Records Found', "link":'AccessCore/Reports/CustomReport','username':username})
        
def Devicewise_Report(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Devices = device.objects.all()
    title = "Devicewise Movement Report"
    url = "AccessCore/Reports/Devicewise_Report_Fun"
    return render_to_response('AccessCore/Range.html',{'Rolefetures':rolefeatures,'projectname':pname,'title':title,'url':url,'Devices':Devices,'username':username})
    
def Devicewise_Report_Fun(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    try:
        txn_list = []
        from1 = str(request.POST['from'])[0:16]+':00'
        to = str(request.POST['to'])[0:16]+':00'
        Device = request.POST.getlist('Devices')
        for i in Device:
            for p in movement.objects.raw('select * from todaymovment where date between \'%s\' and \'%s\' and name = \'%s\' order by id'%(from1,to,i)):
                dic = {}
                dic[1] = p.id
                dic[2] = p.access_id    
                dic[3] = p.accessortype    
                dic[4] = p.status    
                dic[5] = p.uid    
                dic[6] = p.name    
                dic[7] = p.AccessorName 
                dic[8] = p.date
                txn_list.append(dic)
        title = "Devicewise Report"
        table_headings = ['ID','Accessor Code','Accessor Type','Status','UID','Access@','Accessor Name','Date and Time']
        columnfilters = [{'type':"text"} for i in table_headings]
        url = "AccessCore/Reports/Devicewise_Report"
        return render_to_response('AccessCore/Reports_movement_today.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'headings':table_headings,'title':title,'url':url,'columnfilters':columnfilters,'username':username})
    except Exception:
        return render_to_response('AccessCore/user_response.html',{"Rolefetures":rolefeatures,"projectname":pname,"msg":'No Records Found', "link":'AccessCore/Reports/Devicewise_Report','username':username})
        
def Expired_Cards(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    try:
        txn_list = []
        date = str(datetime.now())[0:10]
        obj = card.objects.all()
        for i in obj:
            for p in accessor.objects.raw('select ACAM.id,AC.cardnumber,AA.access_id,AA.AccessorType,AC.expirydate,coalesce(AP.departmentid_id, AV.departmentid_id) AS Department from accesscore_card_To_accessor_map_accessor ACAM\
            left join accesscore_card_to_accessor_map CAP on CAP.id = ACAM.card_to_accessor_map_id\
            left join accesscore_card AC on AC.id = CAP.card_id\
            left join accesscore_accessor AA on AA.id = ACAM.accessor_id \
            left join accesscore_person AP on AP.UserID = AA.access_id\
            left join accesscore_vehicle AV on AV.vehicle_number = AA.access_id where AC.cardnumber = \'%s\' and  \'%s\' > AC.expirydate'%(i,date)):
                dic = {}
                dic[1] = p.cardnumber
                dic[2] = p.access_id
                dic[3] = p.accessortype
                dic[4] = p.expirydate
                a = department.objects.get(id = p.Department)
                dic[5] = a.name
                txn_list.append(dic)
        title = "Expiry Cards Report"
        table_headings = ['Card Number','Accessor','Accessor Type','Expiry Date','Department']
        columnfilters = [{'type':"text"} for i in table_headings]
        url = "uam/home"
        return render_to_response('AccessCore/Reports_movement_today.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'headings':table_headings,'title':title,'url':url,'columnfilters':columnfilters,'username':username})
    except Exception:
        return render_to_response('AccessCore/user_response.html',{"Rolefetures":rolefeatures,"projectname":pname,"msg":'No Records Found', "link":'AccessCore/Reports/Devicewise_Report','username':username})
    
def InvalidAccess(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    try:
        txn_list = []
        for p in movement.objects.raw('select * from todaymovment where Status = "Not Allowed"'):
            dic = {}
            dic[1] = p.id
            dic[2] = p.access_id    
            dic[3] = p.accessortype    
            dic[4] = p.status    
            dic[5] = p.uid    
            dic[6] = p.name    
            dic[7] = p.AccessorName 
            dic[8] = p.date
            txn_list.append(dic)
        title = "Invalid Access Report"
        table_headings = ['ID','Accessor Code','Accessor Type','Status','UID','Access@','Accessor Name','Date & Time']
        columnfilters = [{'type':"text"} for i in table_headings]
        url = "uam/home"
        return render_to_response('AccessCore/Reports_movement_today.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'headings':table_headings,'title':title,'url':url,'columnfilters':columnfilters,'username':username})
    except Exception:
        return render_to_response('AccessCore/user_response.html',{"Rolefetures":rolefeatures,"projectname":pname,"msg":'No Records Found', "link":'uam/home','username':username})
        
def CardsGoingtoExpire(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    title = "Cards Going To Be Expired In N Days  Report"
    Cards  = "Cards"
    url = "AccessCore/Reports/CardsGoingtoExpire_Fun"
    return render_to_response('AccessCore/CardsExpiryDays.html',{'Rolefetures':rolefeatures,'projectname':pname,'title':title,'url':url,'username':username,'Cards':Cards})
    
def CardsGoingtoExpire_Fun(request):
    pname = request.session['projectname']
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    try:
        nods = request.POST['days']
        txn_list = []
        u = datetime.now()
        e = u+timedelta(days=int(nods))
        obj = card.objects.all()
        for i in obj:
            for p in accessor.objects.raw("select ACAM.id,AC.cardnumber,AA.access_id,AA.AccessorType,AC.expirydate,coalesce(AP.departmentid_id, AV.departmentid_id) AS Department from accesscore_card_To_accessor_map_accessor ACAM\
            left join accesscore_card_to_accessor_map CAP on CAP.id = ACAM.card_to_accessor_map_id\
            left join accesscore_card AC on AC.id = CAP.card_id\
            left join accesscore_accessor AA on AA.id = ACAM.accessor_id \
            left join accesscore_person AP on AP.UserID = AA.access_id\
            left join accesscore_vehicle AV on AV.vehicle_number = AA.access_id where AC.cardnumber = \'%s\' and  AC.expirydate between \'%s\' and \'%s\' "%(i,str(u)[0:10],str(e)[0:10])):
                dic = {}
                dic[1] = p.cardnumber
                dic[2] = p.access_id
                dic[3] = p.accessortype
                dic[4] = p.expirydate
                a = department.objects.get(id = p.department)
                dic[5] = a.name
                txn_list.append(dic) 
        title = "Cards going to be expired in next "+str(nods)+" days Report"
        table_headings = ['Card Number','Accessor','Accessor Type','Expiry Date','Department']
        columnfilters = [{'type':"text"} for i in table_headings]
        url = "AccessCore/Reports/CardsGoingtoExpire"
        return render_to_response('AccessCore/Reports_movement_today.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'headings':table_headings,'title':title,'url':url,'columnfilters':columnfilters,'username':username})
    except Exception:
        return render_to_response('AccessCore/user_response.html',{"Rolefetures":rolefeatures,"projectname":pname,"msg":'No Records Found', "link":'uam/home','username':username})


def UMPersonDetails(request):
    pname = request.session['projectname']
    level = request.session['level'] 
    rolefeatures = request.session['Rolefetures']
    username = request.session['username']
    Data = person.objects.all()
    msg = "Please check the details"
    txn_list = []
    try: 
        Did = request.session['id']
        obj = person.objects.get(id = Did)
        name = obj.first_name
        del request.session['id']
        msg = 'Person ' +name+' Successfully Edited'    
    except Exception:
        pass
    try:
        Newid = request.session['txn.id']
        obj = person.objects.get(id = Newid)
        name = obj.first_name
        del request.session['txn.id']
        msg = 'Person ' +name+' Successfully Added'
    except Exception:
        pass
    try:
        delete = request.session['deleteid']
        obj = person.objects.all().values('id')
        if delete not in obj:
            del request.session['deleteid']
            msg = 'Person Successfully Deleted'
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
        dic['UserID'] = Data[i].personid
        dic['First_Name'] = Data[i].first_name
        dic['Last_Name'] = Data[i].last_name
        dic['Disp_Name'] = Data[i].disp_name
        dic['departmentid'] = Data[i].departmentid
        dic['person_type'] = Data[i].persontype
        dic['Gender'] = Data[i].gender
        dic['Address'] = Data[i].address
        dic['City'] = Data[i].city
        dic['Country'] = Data[i].country
        dic['Primary_Email'] = Data[i].primary_email
        dic['Secondary_Email'] = Data[i].secondary_email
        txn_list.append(dic)
    paginator = Paginator(txn_list,5)           
    title = "Persons List"
    return render_to_response('AccessCore/PersonDetails.html',{'report_list':txn_list,'Rolefetures':rolefeatures,'projectname':pname,'title':title,"msg":msg,'username':username})
    
    
    
def shiva(request):
    name = request.POST['name']
    print name
    try:
        personobj = person.objects.get(id=id)
        request.session['deleteid'] = id
        accsrdel = accessor.objects.filter(access_id=personobj.userid).delete()
        f = person.objects.filter(id=id).delete()
        com_feature_field_values.objects.filter(entityvalueid=id).delete()
        return HttpResponseRedirect('/AccessCore/Forms/PersonDetails')
    except Exception:
        message = "Cannot Delete Row,it is used in another table"
        request.session['message'] = message
        return HttpResponseRedirect('/AccessCore/Forms/PersonDetails')    
    