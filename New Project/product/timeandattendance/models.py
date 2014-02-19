from django.db import models
from django.contrib import admin
from accesscore.models import *

# Create your models here.
class shift_type(models.Model):
    name = models.CharField(max_length=30,unique=True)
    code = models.CharField(max_length=30, null = True, blank = True)
    description = models.CharField(max_length = 100, null = True, blank = True)
    fromtime = models.TimeField()
    totime = models.TimeField()
    day_change = models.IntegerField()
    breakstarttime = models.TimeField()
    breakendtime = models.TimeField()
    # is_holiday = models.BooleanField(Defualt = 'No')
    createdbyuserid = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modifiedbyuserid = models.IntegerField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s' %(self.name)
    class Meta:
        verbose_name_plural = "Shift Details"
        
class workday_schedule(models.Model):
    name = models.CharField(max_length=30,unique=True)
    code = models.CharField(max_length=30, null = True, blank = True)
    description = models.CharField(max_length = 100, null = True, blank = True)
    # personid = models.ForeignKey(person)
    # shift_typeid = models.ForeignKey(shift_type)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    # dayofweek = models.CharField(max_length=30)
    # enddate = models.DateTimeField()
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s' %(self.startdate,self.enddate)
    class Meta:
        verbose_name_plural = "Workday Schedule"
    
class shifttype_schedule_map(models.Model):
    shift_type = models.ForeignKey(shift_type)
    schedule = models.ForeignKey(workday_schedule)
    dayofweek = models.CharField(max_length=30)
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s''-''%s' %(self.shift_type,self.schedule,self.dayofweek)
    class Meta:
        verbose_name_plural = "Shifttype Schedule Map"
    
class person_workday_schedule_map(models.Model):
    personid = models.ForeignKey(person)
    workday_schedule = models.ForeignKey(workday_schedule)
    # shift_typeid = models.ForeignKey(shift_type)
    # startdate = models.DateTimeField()
    # enddate = models.DateTimeField()
    class Admin:
        pass
    def __str__(self):
        return '%s''--''%s' %(self.personid.self.shift_typeid)
    class Meta:
        verbose_name_plural = "Person-Schedule Map"
        
        
class attendance_summary(models.Model):
    dayofduty = models.DateField(auto_now_add=True)
    day = models.CharField(max_length=300)
    personid = models.IntegerField()
    shiftname = models.CharField(max_length = 100, null = True, blank = True)
    shiftstarttime = models.CharField(max_length = 100, null = True, blank = True)
    shiftstartendtime = models.CharField(max_length = 100, null = True, blank = True)
    firstlogin = models.DateTimeField(auto_now_add=True)
    lastlogout = models.DateTimeField(auto_now_add=True)
    earlyin = models.CharField(max_length = 100, null = True, blank = True)
    earlyout = models.CharField(max_length = 100, null = True, blank = True)
    latein = models.CharField(max_length = 100, null = True, blank = True)
    lateout = models.CharField(max_length = 100, null = True, blank = True)
    totalworking = models.CharField(max_length = 100, null = True, blank = True)
    lastaction = models.CharField(max_length = 100, null = True, blank = True)
    createdbyuserid = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modifiedbyuserid = models.IntegerField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Admin:
        pass
    def __str__(self):
        return '%s' %(self.personid)
    class Meta:
        verbose_name_plural = "Attendance Summary"