# Create your views here.
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from uam.models import *
######################################################
# from projectone.models import *
from django.db.models import Count
import pylab as p
from pylab import *
from product import settings
import json
from django.utils import simplejson
import os
from django.template import RequestContext, loader
######################################################


#from django.contrib.auth import authenticate, login
#from django.utils import simplejson
from django.db import connection
from django.contrib.auth.hashers import PBKDF2PasswordHasher,MD5PasswordHasher
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate
# from passlib.hash import sha256_crypt,pbkdf2_sha256
def login(request):
    return render_to_response('UAM/login.html')
    
def setting(request):
    
    if request.method == "POST":
        dropdo= request.POST['title']
        role = roles.objects.all()
        selectedrole = roles.objects.get(id = int(request.POST['title']))
        Group = menu.objects.filter(parent__isnull=True)
        # Subgroup = menu.objects.filter(Type="SG")
        Subgroup = menu.objects.all()
        # Items = menu.objects.filter(Type="F")
        Items = menu.objects.all()
        print "haaaaaaaaaai"
        print "post value",request.POST['title']
        role_menu_obj=role_to_menu.objects.filter(role_id = int(request.POST['title']))
        print "role_menu_obj",role_menu_obj
        rolemenu_menuobj = []
        for i in range(len(role_menu_obj)):
            print "the menu_id are", rolemenu_menuobj.append(role_menu_obj[i].menu)
        print "rolemenu menu obj",rolemenu_menuobj
        role_parent = []
        for i in range(len(role_menu_obj)):
            print "the main menu id's are",role_parent.append(role_menu_obj[i].menu.parent)
        print "rollllllllll",role_parent
        return render_to_response('UAM/setting2.html',{'role':role,'selectedrole':selectedrole,'Feature_Subgroup':Subgroup,'Feature_Group':Group,'Feature_Items':Items,'menu_id':rolemenu_menuobj,'main_menu':role_parent})
    else:
        role = roles.objects.all()
        return render_to_response('UAM/setting2.html',{'role':role})
        # return render_to_response('UAM/setting2.html',{'role':role,'Feature_Subgroup':Subgroup,'Feature_Group':Group,'Feature_Items':Items,'menu_id':rolemenu_menuobj,'main_menu':role_parent})

def adminlogin(request):
    return render_to_response('UAM/admin_login.html')

def config(request):
    role = request.POST['role']
    x = []
    x = request.POST.getlist('check')
    roleinstance = roles.objects.get(id__exact=int(role))
    group =[]
    role_obj = role_to_menu.objects.filter(role = roleinstance).delete()
    for i in range(len(x)):
        menuobj = menu.objects.get(id__exact=int(x[i]))
        if role_to_menu.objects.filter(menu=menuobj.id,role=roleinstance.id).count() > 0:
            pass
        else:
            role_to_menu(role = roleinstance,menu = menuobj,Status = 'yes').save()            
    return render_to_response('UAM/entry.html',{'role':roleinstance.Role_Name})

def authent(request):
    username = request.POST['username'] 
    passw = request.POST['password']
    request.session['username']=username
    username = request.session['username'] 
    level = 3
    msg = "Please Provide Correct Username and Password"
    grouplist = []
    subgrouplist = []
    feature_list = []
    try:
        userobject = user.objects.get(user_name = username)
        userid = userobject.id
        request.session['userid']= userid
        userrole = user_role_map.objects.get(user_id_id = userid)
        role_id = userrole.role_id_id
        request.session['roleid'] = role_id
        if userobject.check_password(passw):
            projectname = userrole.role_id.product.name
            request.session['projectname'] = projectname
            request.session['level'] = level       
            Rolefetures = role_to_menu.objects.filter(role__id=role_id)
            request.session['Rolefetures'] = Rolefetures
            return render_to_response('UAM/index.html',{'test1':"shiva",'test2':"shiva","username":user,"projectname":projectname,"level":"3","Rolefetures":Rolefetures,'userid':userid,"username":username})
        else:
            return render_to_response('UAM/login.html',{'msg':msg})
    except Exception:
        return render_to_response('UAM/login.html',{'msg':msg})
        

def home(request):
    pname =request.session['projectname']
    Rolefetures = request.session['Rolefetures']
    username = request.session['username']
    return render_to_response('UAM/index.html',{"projectname":pname,"Rolefetures":Rolefetures,"username":username})



def daily(request):
    return HttpResponse ('daily')
def logout_view(request):
    if 'projectname' in request.session and 'username' in request.session and 'Rolefetures' in request.session :
        try:
            
            del request.session['projectname']
            del request.session['username']
            del request.session['Rolefetures']
            request.session.flush()
        except KeyError:
            pass    
    return render_to_response('UAM/login.html')
    
################ to get encrypt password ###########

# for p in bc.objects.raw('select id,des_decrypt(password) pwd from uam_bc'):
    # print "passwords",(p.pwd)
    
    
#   index
def index(request):
    # create context dictionary
    context = {}
    # variables...
    context['form'] = SearchForm()
    return render(request, 'index.html', context)
 
 
#   find_cities (ajax processor)   
def find_cities(request, qs=None):
    if qs is None:
        qs = Country.objects.values_list('name', flat=True).all()
    # if request.GET.get('country_name'):
        # country_name=request.GET.get('country_name')
    # # create an empty list to hold the results
    # results = []
    # qs = Country.objects.values_list('name', flat=True).filter(name=country_name).order_by('name')
    # # iterate over each city and append to results list 
    # for city in qs:
        # results.append(city)
    # # if no results found then append a relevant message to results list
    # if not results:
        # # if no results then dispay empty message
        # results.append(_("No cities found")) 
    # # return JSON object
    # return HttpResponse(simplejson.dumps(results))    