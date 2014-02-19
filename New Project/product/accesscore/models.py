from django.db import models
from django.contrib import admin
from uam.models import *
#from test.test_imageop import MAX_LEN

STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    
GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

FIELD_TYPE_CHOICES = (
        (1, 'String'),
        (2, 'Integer'),
        (3, 'Boolean'),
        (4, 'Double'),
        (5, 'DateTime'),
        (6, 'LIST'),
    )


    
class com_entity(models.Model):
    table = models.CharField(max_length=30,unique=True)
    description = models.CharField(max_length = 100, null = True, blank = True)
    class Admin:
        pass
    def __str__(self):
        return '%s' %(self.Table)
    class Meta:
        verbose_name_plural = "COM_Entity"
        db_table = "com_entity"
    
class com_feature_fields(models.Model):
    fieldname = models.CharField(max_length=30)
    field_type = models.IntegerField(max_length=10,choices=FIELD_TYPE_CHOICES)
    status = models.CharField(max_length = 30, choices = STATUS_CHOICES)
    feature_table = models.ForeignKey(com_entity,on_delete=models.PROTECT)
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s' %(self.fieldname,self.feature_table)
    class Meta:
        verbose_name_plural = "COM_Feature_Fields"
        db_table = "com_feature_fields"

class com_feature_field_values(models.Model):
    # entityid = models.ForeignKey(COM_Entity)
    entityvalueid = models.CharField(max_length=30)
    feature_field = models.ForeignKey(com_feature_fields,on_delete=models.PROTECT)
    Stringvalue = models.CharField(max_length=30, null = True, blank = True)
    Integergvalue = models.IntegerField(max_length=10, null = True, blank = True)
    DateTimevalue = models.DateTimeField(null=True, blank=True)
    Doublevalue = models.FloatField(null=True, blank=True)
    Booleanvalue = models.CharField(max_length=30,null=True, blank=True)
    Listvalue = models.CharField(max_length=30,null=True, blank=True)
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s' %(self.entityvalueid,self.feature_field)
    class Meta:
        verbose_name_plural = "COM_Feature_Field_Values"
        db_table = "com_feature_field_values"
    
class com_list(models.Model):
    feature_field = models.ForeignKey(com_feature_fields,on_delete=models.PROTECT)
    dropdownvalue = models.CharField(max_length=30)
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s' %(self.feature_field,self.dropdownvalue)
    class Meta:
        verbose_name_plural = "COM_List"
        db_table = "com_list"
    
class company(models.Model):
    name = models.CharField(max_length=30,unique=True, db_column=u'Name')
    code = models.CharField(max_length=30, null = True, blank = True)
    description = models.CharField(max_length = 100, null = True, blank = True)
    createdbyuserid = models.IntegerField(null=True, blank=True) 
    createddate = models.DateTimeField(auto_now_add=True)
    modifiedbyuserid = models.IntegerField(null=True, blank=True) 
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s' %(self.name)
    class Meta:
        verbose_name_plural = "Company"
    
class department(models.Model):
    name = models.CharField(max_length=30,unique=True)
    companyid = models.ForeignKey(company,on_delete=models.PROTECT)
    code = models.CharField(max_length=30,null = True, blank = True)
    description = models.CharField(max_length = 100, null = True, blank = True)
    createdbyuserid = models.IntegerField(null=True, blank=True)
    createddate = models.DateTimeField(auto_now_add=True)
    modifiedbyuserid = models.IntegerField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s' %(self.name,self.companyid)
    class Meta:
        verbose_name_plural = "Department"
    
class person_type(models.Model):
    name = models.CharField(max_length=30,unique = True)
    code = models.CharField(max_length=30, null = True, blank = True)
    description = models.CharField(max_length = 100, null = True, blank = True)
    createdbyuserid = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modifiedbyuserid = models.IntegerField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s' %(self.name)
    class Meta:
        verbose_name_plural = "Person Type"
    
class person(models.Model):
    personid = models.CharField(max_length=30,unique = True)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30,null=True, blank = True)
    disp_name=models.CharField(max_length=30,null=True, blank = True)
    departmentid = models.ForeignKey(department,on_delete=models.PROTECT)
    persontype = models.ForeignKey(person_type,on_delete=models.PROTECT)
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES)
    address = models.CharField(max_length=30, null=True, blank = True)
    city = models.CharField(max_length=30, null=True, blank = True)
    country = models.CharField(max_length=30, null=True, blank = True) 
    primary_email = models.EmailField()
    secondary_email = models.EmailField(null=True, blank = True)
    user = models.ForeignKey(user,null=True, blank = True,on_delete=models.PROTECT)
    manager = models.ForeignKey('self',null=True, blank = True,on_delete=models.PROTECT)
    code = models.CharField(max_length=30, null = True, blank = True)
    description = models.CharField(max_length = 100, null = True, blank = True)
    createdbyuserid = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modifiedbyuserid = models.IntegerField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s' %(self.personid,self.first_name)
    class Meta:
        verbose_name_plural = "Person"
    
class uamuser_person_map(models.Model):
    user = models.ForeignKey(user,on_delete=models.PROTECT)
    person = models.ForeignKey(person,on_delete=models.PROTECT)
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s' %(self.user,self.person)
    class Meta:
        verbose_name_plural = "User-Person Map"
        
class vehicle_type(models.Model):
    name = models.CharField(max_length=30,unique = True)
    code = models.CharField(max_length=30, null = True, blank = True)
    description = models.CharField(max_length = 100, null = True, blank = True)
    createdbyuserid = models.IntegerField(null=True, blank=True)
    createddate = models.DateTimeField(auto_now_add=True)
    modifiedbyuserid = models.IntegerField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s' %(self.name)
    class Meta:
        verbose_name_plural = "Vehicle Type"
    
class vehicle(models.Model):
    vehicle_number = models.CharField(max_length=30,unique = True)
    type = models.ForeignKey(vehicle_type,on_delete=models.PROTECT)
    departmentid = models.ForeignKey(department,on_delete=models.PROTECT)
    code = models.CharField(max_length=30, null = True, blank = True)
    description = models.CharField(max_length = 100, null = True, blank = True)
    createdbyuserid = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modifiedbyuserid = models.IntegerField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s' %(self.vehicle_number,self.type)
    class Meta:
        verbose_name_plural = "Vehicle"
        
TYPE_CHOICES = (
        ('Person', 'Person'),
        ('Vehicle', 'Vehicle'),
    )
class accessor(models.Model):
    access_id = models.CharField(max_length=30)
    accessortype = models.CharField(max_length=30,choices=TYPE_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s' %(self.access_id,self.accessortype)
    class Meta:
        # unique_together = ('access_id','AccessorType')
        verbose_name_plural = "Accessor Information"
    
class card(models.Model):
    cardnumber = models.CharField(max_length=30,unique=True)
    startdate = models.DateField()
    expirydate = models.DateField()
    pin = models.CharField(max_length=30,null=True, blank=True)
    status = models.CharField(max_length=30,choices=STATUS_CHOICES)
    createdbyuserid = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modifiedbyuserid = models.IntegerField(null=True, blank=True) 
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s' %(self.cardnumber)
    class Meta:
        verbose_name_plural = "Card Information"
    
class card_to_accessor_map(models.Model):
    card = models.ForeignKey(card,unique = True,on_delete=models.PROTECT)
    accessor = models.ManyToManyField(accessor)
    createdbyuserid = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modifiedbyuserid = models.IntegerField(null=True, blank=True) 
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s' %(self.card)
    class Meta:
        verbose_name_plural = "Card To Accessor Map"

class device(models.Model):
    name = models.CharField(max_length=30)
    macaddress = models.CharField(max_length=30,unique=True)
    ipaddress = models.CharField(max_length=30,unique=True)
    hostname = models.CharField(max_length=30)
    devicetype = models.CharField(max_length=30)
    departmentid = models.ForeignKey(department,on_delete=models.PROTECT)
    createdbyuserid = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modifiedbyuserid = models.IntegerField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s' %(self.name)
    class Meta:
        verbose_name_plural = "Device"

class schedule(models.Model):
    name = models.CharField(max_length=30,unique=True)
    starttime = models.TimeField()
    endtime = models.TimeField()
    monday = models.NullBooleanField(null=True, blank=True) # Field name made lowercase.
    tuesday = models.NullBooleanField(null=True, blank=True) # Field name made lowercase.
    wednesday = models.NullBooleanField(null=True, blank=True) # Field name made lowercase.
    thursday = models.NullBooleanField(null=True, blank=True) # Field name made lowercase.
    friday = models.NullBooleanField(null=True, blank=True) # Field name made lowercase.
    saturday = models.NullBooleanField(null=True, blank=True) # Field name made lowercase.
    sunday = models.NullBooleanField(null=True, blank=True) # Field name made lowercase.
    createdbyuserid = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modifiedbyuserid = models.IntegerField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s' %(self.name)
    class Meta:
        verbose_name_plural = "Schedule Details"
    
class devicegroup(models.Model):
    name = models.CharField(max_length=30,unique=True)
    deviceid = models.ManyToManyField(device)
    createdbyuserid = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modifiedbyuserid = models.IntegerField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s' %(self.name)
    class Meta:
        verbose_name_plural = "Device Group"
        

    
class accessgroup(models.Model):
    name = models.CharField(max_length=30, null = True, blank = True)
    devicegroup = models.ForeignKey(devicegroup,on_delete=models.PROTECT)
    scheduleid = models.ForeignKey(schedule,on_delete=models.PROTECT)
    createdbyuserid = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modifiedbyuserid = models.IntegerField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s' %(self.name)
    class Meta:
        verbose_name_plural = "Access Group"
    
class accessgroupassigntocard(models.Model):
    cardid = models.ForeignKey(card,unique = True,on_delete=models.PROTECT)
    departmentid = models.ForeignKey(department,on_delete=models.PROTECT)
    accessgroupid = models.ForeignKey(accessgroup,on_delete=models.PROTECT)
    createdbyuserid = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modifiedbyuserid = models.IntegerField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s''--''%s' %(self.cardid,self.departmentid,self.accessgroupid)
    class Meta:
        verbose_name_plural = "Access Group Assigned to Card"
    
class movement(models.Model):
    accessorid = models.ForeignKey(accessor, null = True, blank = True,on_delete=models.PROTECT)
    accessorcode = models.CharField(max_length = 30, null = True, blank = True)
    deviceid = models.ForeignKey(device,on_delete=models.PROTECT)
    accessortype = models.CharField(max_length = 30, null = True, blank = True)
    date = models.DateTimeField()
    uid = models.CharField(max_length = 30, null = True, blank = True)
    statusname = models.CharField(max_length = 30)
    status = models.CharField(max_length = 30)
    description = models.CharField(max_length = 100, null = True, blank = True)
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s' %(self.deviceid,self.accessorid)
    class Meta:
        verbose_name_plural = "Movement"
    
