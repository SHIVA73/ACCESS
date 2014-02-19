from django.db import models
from django.contrib import admin
from accesscore.models import *
# Create your models here.
class holiday(models.Model):
    name = models.TextField()
    fromdate = models.DateTimeField()
    todate = models.DateTimeField()
    createdbypersonid = models.IntegerField()
    createddate = models.DateTimeField()
    modifiedbypersonid = models.IntegerField()
    modifieddate = models.DateTimeField()
    version_ts = models.TextField()
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s' %(self.fromdate,self.todate)
    class Meta:
        verbose_name_plural = "Holiday"
class leavetype(models.Model):
    code = models.CharField(unique=True, max_length=15)
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=45,null=True, blank=True)
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s' %(self.code,self.name)
    class Meta:
        verbose_name_plural = "Leave Type"
    
class leavesetup(models.Model):
    leavetype = models.ForeignKey(leavetype,on_delete=models.PROTECT)
    persontype = models.ForeignKey(person_type,on_delete=models.PROTECT)
    numberofdays = models.IntegerField()
    description = models.CharField(max_length=45,null=True, blank=True)
    class Admin:
        pass
    class Meta:
        unique_together = ("leavetype", "persontype")
    class Meta:
        verbose_name_plural = "Leave Setup"
   
STATUS_CHOICES = (
        (0, 'Applied'),
        (1, 'Approved'),
        (2, 'Cancel'),
        (3, 'Rejected'),
    )
    
class leaveapply(models.Model):
    person = models.ForeignKey(person,on_delete=models.PROTECT)
    startdate = models.DateField()
    enddate = models.DateField()
    numberofdays = models.FloatField(null=True, blank=True)
    description = models.TextField(max_length=45,null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES)
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s' %(self.person,self.status)
    class Meta:
        verbose_name_plural = "Leave Apply"
        
TYPE_CHOICES = (
        (0, 'Int Value'),
        (1, 'Char Value'),
        (2, 'Date Value'),
        (3, 'Double Value'),
    )
class comp_off(models.Model):
    person = models.ForeignKey(person,on_delete=models.PROTECT)
    numberofdays = models.FloatField()
    createdby = models.CharField(max_length=15)
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s''--''%s' %(self.empid,self.numberofdays,self.createdby)
    class Meta:
        verbose_name_plural = "Compensation Off"