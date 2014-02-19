from django import forms
 
class SearchForm(forms.Form):
    country = forms.ModelChoiceField(
                queryset=Country.objects.values_list('name'), 
                empty_label='Not Specified', 
                widget=forms.Select(attrs={ 
                                   "onChange":'getCity()'})
                )
 
    city = forms.ModelChoiceField(
                queryset=Country.objects.values_list('city'), 
                empty_label='Not Specified'
                )