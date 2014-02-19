from django import forms
from django.forms import ModelForm
from accesscore.widgets import *  
from models import *
import datetime
from django.forms import TextInput, Textarea

class Companyform(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Companyform, self).__init__(*args, **kwargs)
        obj_ = com_feature_fields.objects.filter(feature_table__table = 'Company',status = 'Active')
        for i in obj_:    
            saving(self,i.field_type,i.fieldname)
    class Meta:
        model = company
        exclude = ('createdbyuserid','modifiedbyuserid',)
        
        
class Departmentform(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Departmentform, self).__init__(*args, **kwargs)
        obj_ = com_feature_fields.objects.filter(feature_table__table = 'Department',status = 'Active')
        for i in obj_:    
            saving(self,i.field_type,i.fieldname)
        self.fields['companyid'].label = "Company Name"
    class Meta:
        model = department
        exclude = ('createdbyuserid','modifiedbyuserid',)

class Person_Typeform(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Person_Typeform, self).__init__(*args, **kwargs)
        obj_ = com_feature_fields.objects.filter(feature_table__table = 'Person_Type',status = 'Active')
        for i in obj_:    
            saving(self,i.field_type,i.fieldname)
    class Meta:
        model = person_type
        exclude = ('createdbyuserid','modifiedbyuserid',)
    
class Personform(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Personform, self).__init__(*args, **kwargs)
        obj_ = com_feature_fields.objects.filter(feature_table__table = 'Person',status = 'Active')
        for i in obj_:    
            saving(self,i.field_type,i.fieldname)
        self.fields['departmentid'].label = "Department Name"
        self.fields['disp_name'].label = "Display Name"
    class Meta:
        model = person
        exclude = ('createdbyuserid','modifiedbyuserid',)
               
class Vehicleform(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Vehicleform, self).__init__(*args, **kwargs)
        obj_ = com_feature_fields.objects.filter(feature_table__table = 'Vehicle',status = 'Active')
        for i in obj_:    
            saving(self,i.field_type,i.fieldname)
    
    class Meta:
        model = vehicle
        exclude = ('createdbyuserid','modifiedbyuserid',)
        
        
class Cardform(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Cardform, self).__init__(*args, **kwargs)
        obj_ = com_feature_fields.objects.filter(feature_table__table = 'Card',status = 'Active')
        for i in obj_:    
            saving(self,i.field_type,i.fieldname)
    
    class Meta:
        model = card
        widgets = {
            'startdate': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD','class':'date'}),
            'expirydate': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD','class':'date'}),
            }
        exclude = ('createdbyuserid','modifiedbyuserid',)
    def clean(self):
        cleaned_data = self.cleaned_data
        startdate = cleaned_data.get('startdate')
        expirydate = cleaned_data.get('expirydate')
        try:
            if  self.cleaned_data['startdate'] > self.cleaned_data['expirydate']:
                msg = u"Start Date Should Less Than Expiry Date"
                self._errors["startdate"] = self.error_class([msg])
                del cleaned_data["startdate"]
                raise ValidationError(msg)
            else:
                return self.cleaned_data
        except Exception:
            return self.cleaned_data
    
class Deviceform(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Deviceform, self).__init__(*args, **kwargs)
        obj_ = com_feature_fields.objects.filter(feature_table__table = 'Device',status = 'Active')
        for i in obj_:    
            saving(self,i.field_type,i.fieldname)
    class Meta:
        model = device
        exclude = ('createdbyuserid','modifiedbyuserid',)
        
class Vehicle_Typeform(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Vehicle_Typeform, self).__init__(*args, **kwargs)
        obj_ = com_feature_fields.objects.filter(feature_table__table = 'Vehicle_Type',status = 'Active')
        for i in obj_:    
            saving(self,i.field_type,i.fieldname)
    class Meta:
        model = vehicle_type
        exclude = ('createdbyuserid','modifiedbyuserid',)
        
class DeviceGroupform(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviceGroupform, self).__init__(*args, **kwargs)
        obj_ = com_feature_fields.objects.filter(feature_table__table = 'Devicegroup',status = 'Active')
        for i in obj_:    
            saving(self,i.field_type,i.fieldname)
    class Meta:
        model = devicegroup
        exclude = ('createdbyuserid','modifiedbyuserid',)
        
class Scheduleform(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Scheduleform, self).__init__(*args, **kwargs)
        obj_ = com_feature_fields.objects.filter(feature_table__table = 'Schedule',status = 'Active')
        for i in obj_:    
            saving(self,i.field_type,i.fieldname)
    starttime =  forms.TimeField(widget=SelectTimeWidget)
    endtime =  forms.TimeField(widget=SelectTimeWidget)
    class Meta:
        model = schedule
        exclude = ('createdbyuserid','modifiedbyuserid',)
        
class Accessgroupform(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Accessgroupform, self).__init__(*args, **kwargs)
        obj_ = com_feature_fields.objects.filter(feature_table__table = 'Accessgroup',status = 'Active')
        for i in obj_:    
            saving(self,i.field_type,i.fieldname)
    class Meta:
        model = accessgroup
        exclude = ('createdbyuserid','modifiedbyuserid',)
        
class Accessgroupassigntocardform(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Accessgroupassigntocardform, self).__init__(*args, **kwargs)
        obj_ = com_feature_fields.objects.filter(feature_table__table = 'Accessgroupassigntocard',status = 'Active')
        for i in obj_:    
            saving(self,i.field_type,i.fieldname)
    class Meta:
        model = accessgroupassigntocard
        exclude = ('createdbyuserid','modifiedbyuserid',)
        
class CardtoAccessorform(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CardtoAccessorform, self).__init__(*args, **kwargs)
        obj_ = com_feature_fields.objects.filter(feature_table__table = 'Card_To_Accessor_Map',status = 'Active')
        for i in obj_:    
            saving(self,i.field_type,i.fieldname)
    class Meta:
        model = card_to_accessor_map
        exclude = ('createdbyuserid','modifiedbyuserid',)
        
# class Entityform(ModelForm):
    # class Meta:
        # model = COM_Entity
        
class Fieldsform(ModelForm):
    class Meta:
        model = com_feature_fields
        
# class Fieldvaluesform(ModelForm):
    # class Meta:
        # model = COM_Feature_Field_Values
        # exclude = ('entityvalueid','feature_field',)
        
class Listform(ModelForm):
    class Meta:
        model = com_list
        
def saving(self,value,a):
    if value == 1:
        self.fields[a] = forms.CharField(required=False)
    if value == 2:
        self.fields[a] = forms.IntegerField(required=False)
    if value == 3:
        self.fields[a] = forms.NullBooleanField(required=False)
    if value == 4:
        self.fields[a] = forms.FloatField(required=False)
    if value == 5:
        self.fields[a] = forms.DateTimeField(required=False,initial=datetime.datetime.now())
    if value == 6:
        # self.fields[a] = forms.ChoiceField(COM_List.objects.filter(feature_field__feature_table__table = table))
        aba = com_list.objects.filter(feature_field__fieldname = a)
        self.fields[a] = forms.ModelChoiceField(aba,required=False)
		
class User_Person_Mapform(ModelForm):
    class Meta:
        model = uamuser_person_map
            
        