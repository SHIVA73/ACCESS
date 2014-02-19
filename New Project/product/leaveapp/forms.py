from django import forms
from django.forms import ModelForm
# from CLA.widgets import *  
from models import *
from uam.models import *
import datetime
from django.forms import *

# class EmployeeTypeform(ModelForm):
    # class Meta:
        # model = EmployeeType
        
# class Employeeform(ModelForm):
    # def __init__(self, *args, **kwargs):    
        # super(Employeeform, self).__init__(*args, **kwargs)
        # self.fields['dateofjoining'].label = "Date Of Joining"
        # self.fields['employeetype'].label = "Employee Type"
        # self.fields['userid'].label = "User Id"
    # class Meta:
        # model = Employee
        # widgets = {
            # 'dateofjoining': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD','class':'date'}),
            # 'userid': Select(choices=[['', '----------']] + [[r.id, r.First_Name] for r in user.objects.all()]),
            # 'approver':Select(choices=[['', '----------']] + [[r.id, r.name] for r in Employee.objects.all()])
            # }
        
        
class LeaveTypeform(ModelForm):
    class Meta:
        model = leavetype
        
class LeaveSetupform(ModelForm):
    def __init__(self, *args, **kwargs):    
        super(LeaveSetupform, self).__init__(*args, **kwargs)
        self.fields['numberofdays'].label = "Number Of Days"
        self.fields['persontype'].label = "Person Type"
        self.fields['leavetype'].label = "Leave Type"
    class Meta:
        model = leavesetup
    def clean(self):
        """ This is the form's clean method, not a particular field's clean method """
        cleaned_data = self.cleaned_data
        leavetype = cleaned_data.get("leavetype")
        persontype = cleaned_data.get("persontype")

        if leavesetup.objects.filter(leavetype=leavetype, persontype=persontype).count() > 0:
            msg = u"Leave Type and Employee Type combination already exists."
            self._errors["leavetype"] = self.error_class([msg])
            self._errors["persontype"] = self.error_class([msg])
            del cleaned_data["leavetype"]
            del cleaned_data["persontype"]
            raise forms.ValidationError(msg)
        return cleaned_data
        
class LeaveApplyform(ModelForm):
    def __init__(self, *args, **kwargs):    
        super(LeaveApplyform, self).__init__(*args, **kwargs)
        self.fields['startdate'].label = "Start Date"
        self.fields['enddate'].label = "End Date"
        self.fields['status'].choices = [(0,'Applied')]
    class Meta:
        model = leaveapply
        exclude = ('numberofdays',)
        widgets = {
            'startdate': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD','class':'date'}),
            'enddate': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD','class':'date'}),          
            }
        
        
    def clean(self):
        cleaned_data = self.cleaned_data
        startdate = cleaned_data.get('startdate')
        enddate = cleaned_data.get('enddate')
        person = cleaned_data.get('person')
        try:
            if  self.cleaned_data['startdate'] > self.cleaned_data['enddate']:
                msg = u"Start Date Should Less Than Expiry Date"
                self._errors["startdate"] = self.error_class([msg])
                del cleaned_data["startdate"]
                raise ValidationError(msg)
            a = leaveapply.objects.filter(status__in = [0,1],person = self.cleaned_data['person'])
            for i in a:
                if  i.startdate <= self.cleaned_data['startdate'] <= i.enddate:
                    msg = u"Already Applied on this Date"
                    self._errors["startdate"] = self.error_class([msg])
                    del cleaned_data["startdate"]
                    raise ValidationError(msg)
                # else:
                    # return self.cleaned_data
            return self.cleaned_data
        except Exception:
            return self.cleaned_data
        return cleaned_data
            
class Approverform(ModelForm):
    class Meta:
        model = leaveapply
        widgets = {
            'startdate': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD','class':'date'}),
            'enddate': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD','class':'date'}),          
            'person': forms.TextInput(),          
            }
    def __init__(self, *args, **kwargs):    
        super(Approverform, self).__init__(*args, **kwargs)
        self.fields['startdate'].label = "Start Date"
        self.fields['enddate'].label = "End Date"
        self.fields['numberofdays'].label = "Number Of Days"
        self.fields['status'].choices = [(1,'Approved'),(3,'Rejected')]
        
        
        
class Cancelform(ModelForm):
    class Meta:
        model = leaveapply
        widgets = {
            'startdate': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD','class':'date'}),
            'enddate': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD','class':'date'}),     
            'person': forms.TextInput(),  
            }
    def __init__(self, *args, **kwargs):    
        super(Cancelform, self).__init__(*args, **kwargs)
        self.fields['startdate'].label = "Start Date"
        self.fields['enddate'].label = "End Date"
        self.fields['numberofdays'].label = "Number Of Days"
        self.fields['status'].choices = [(2,'Cancel')]
        
class Compoff_form(ModelForm):
    class Meta:
        model = comp_off
        widgets = {
        'createdby':forms.TextInput(attrs={'class':'disabled', 'readonly':'readonly'})
        }
    def __init__(self, *args, **kwargs):    
        super(Compoff_form, self).__init__(*args, **kwargs)
        self.fields['person'].label = "Person"
        self.fields['numberofdays'].label = "Number Of Days"
        self.fields['createdby'].label = "Created By"

    





        

        
            
        