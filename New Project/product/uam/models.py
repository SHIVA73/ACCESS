from django.db import models
from test.test_imageop import MAX_LEN
import re
# import django.contrib.auth.models
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)


from django.utils.translation import ugettext_lazy as _
from django.db import connection

        
    
GROUP_STATUS_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    
class product(models.Model):    
    name=models.CharField(max_length=30)
    status = models.CharField(max_length = 10, choices=GROUP_STATUS_CHOICES)
    description = models.CharField(max_length = 100, null = True, blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s' %(self.name)
    class Meta:
        verbose_name_plural = "Product"
        verbose_name = "Product"
from django.core.exceptions import ValidationError
class roles(models.Model):
    role_name = models.CharField(max_length = 35,verbose_name = "Role")    
    code_name = models.CharField(max_length = 35)
    description = models.CharField(max_length = 100, null = True, blank = True)
    product = models.ForeignKey(product)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s' %(self.role_name)
    class Meta:
        verbose_name_plural = "Role"
        verbose_name = "Role"
   
        
GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
import datetime
from django.utils import timezone
import re 
def special_match(strg, search=re.compile(r'[['']^a-z0-9.!@#$%^&*()--+={};><.,?/"|\]').search):
    return not bool(search(strg))
class user(models.Model):
    # def foo(self,*args):
        # print "hi",self.pk  
    # print "ashd",self.pk
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    disp_name=models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.CharField(max_length=255, null=True, blank = True)
    city = models.CharField(max_length=50, null=True, blank = True)
    country = models.CharField(max_length=50, null=True, blank = True) 
    primary_email = models.EmailField()
    secondary_email = models.EmailField(null=True, blank = True)
    # Mobile = models.BigIntegerField(null=True, blank = True)
    start_date = models.DateField(null=True, blank = True)
    end_date = models.DateField(null=True, blank = True)
    user_name=models.CharField(unique=True,max_length=30)
    password=models.CharField(max_length=150,help_text="Password does not contain special charecters (@#$^&*!?><~}|{+=_-,./\)")
    created_date = models.DateTimeField(auto_now_add=True)
    # modified_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(editable=False,default=timezone.now())
    class Admin:
        pass
    def __str__(self):
        return '%s' %(self.first_name)

    class Meta:
        verbose_name_plural = "User"    
        verbose_name = "User"
    def set_password(self, raw_password):
        # self.Password = make_password(raw_password) 
        print "asdd"      
    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save()
        return check_password(raw_password, self.password, setter)
    def save(self, *args, **kwargs):    
        print "hi", self.password
        self.password = make_password(self.password,None,'pbkdf2_sha256')
        super(user, self).save(*args, **kwargs) 
    
class user_role_map(models.Model):
    user_id = models.ForeignKey(user)
    role_id = models.ForeignKey(roles)
    status=models.CharField(max_length=20, choices=GROUP_STATUS_CHOICES)
    description = models.CharField(max_length = 100, null = True, blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    class Meta:
        verbose_name_plural = "User_Role_Map" 
        verbose_name = "User_Role_Map"
    def __str__(self):
        return '%s ''--''%s' %(self.user_id,self.role_id)   
    def get_query_set(self):
        return super(user_role_map, self).get_query_set().filter(role_id=1)
        
class menuitem(models.Manager):
    def get_query_set(self):
        return super(menuitem, self).get_query_set().filter(Type='F')
        
class menu(models.Model):
    parent= models.ForeignKey('self', null=True, blank=True, related_name='children')
    name=models.CharField(max_length=200)
    type = models.CharField(max_length = 100, null = True, blank = True,default= "F",help_text= "Keep 'F' Only for a feature--or--Keep empty")
    urlname = models.CharField(max_length = 100)
    status = models.CharField(max_length = 100)
    # Access  = models.CharField(max_length = 100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    # menu_item = menuitem()
    class Admin:
        pass
    class Meta:
        verbose_name_plural = "Menu"    
        verbose_name =    "Menu"
    def __str__(self):
        return '%s ''--''%s' %(self.name,self.parent)
    def clean(self):
        print "hoiah"
        try:
            if self.type[0] != 'F':
                raise  ValidationError('Enter F to activate feature or leave empty')
        except IndexError:
            pass
            # else:
                # super(Roles, self).save(*args, **kwargs)    
                

   
    
class role_to_menu(models.Model):
    role= models.ForeignKey(roles)
    menu= models.ForeignKey(menu)
    status = models.CharField(max_length = 100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    class Meta:
        verbose_name_plural = "Role_to_Menu"    
        verbose_name = "Role_to_Menu"  
    def __str__(self):
        return '%s ''--''%s' %(self.role,self.menu)
        

   
