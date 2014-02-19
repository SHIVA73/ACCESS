"""
Extra HTML Widget classes
"""

import datetime
import re
from django import forms
from django.forms.widgets import Widget, Select
from django.utils import datetime_safe
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe
from django.utils.formats import get_format
from django.conf import settings

from django.forms.widgets import Widget, Select, MultiWidget

__all__ = ('SelectDateWidget','SelectTimeWidget')

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')

time_pattern = r'(\d\d?):(\d\d)(:(\d\d))? *([aApP]\.?[mM]\.?)?$'

RE_TIME = re.compile(time_pattern)
# The following are just more readable ways to access re.matched groups:
HOURS = 0
MINUTES = 1
SECONDS = 3
MERIDIEM = 4

def _parse_date_fmt():
    fmt = get_format('DATE_FORMAT')
    escaped = False
    output = []
    for char in fmt:
        if escaped:
            escaped = False
        elif char == '\\':
            escaped = True
        elif char in 'Yy':
            output.append('year')
            #if not self.first_select: self.first_select = 'year'
        elif char in 'bEFMmNn':
            output.append('month')
            #if not self.first_select: self.first_select = 'month'
        elif char in 'dj':
            output.append('day')
            #if not self.first_select: self.first_select = 'day'
    return output

class SelectDateWidget(Widget):
    """
    A Widget that splits date input into three <select> boxes.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """
    none_value = (0, '---')
    month_field = '%s_month'
    day_field = '%s_day'
    year_field = '%s_year'

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year+10)

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, basestring):
                if settings.USE_L10N:
                    try:
                        input_format = get_format('DATE_INPUT_FORMATS')[0]
                        v = datetime.datetime.strptime(value, input_format)
                        year_val, month_val, day_val = v.year, v.month, v.day
                    except ValueError:
                        pass
                else:
                    match = RE_DATE.match(value)
                    if match:
                        year_val, month_val, day_val = [int(v) for v in match.groups()]
        choices = [(i, i) for i in self.years]
        year_html = self.create_select(name, self.year_field, value, year_val, choices)
        choices = MONTHS.items()
        month_html = self.create_select(name, self.month_field, value, month_val, choices)
        choices = [(i, i) for i in range(1, 32)]
        day_html = self.create_select(name, self.day_field, value, day_val,  choices)

        output = []
        for field in _parse_date_fmt():
            if field == 'year':
                output.append(year_html)
            elif field == 'month':
                output.append(month_html)
            elif field == 'day':
                output.append(day_html)
        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        first_select = None
        field_list = _parse_date_fmt()
        if field_list:
            first_select = field_list[0]
        if first_select is not None:
            return '%s_%s' % (id_, first_select)
        else:
            return '%s_month' % id_

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)
        if y == m == d == "0":
            return None
        if y and m and d:
            if settings.USE_L10N:
                input_format = get_format('DATE_INPUT_FORMATS')[0]
                try:
                    date_value = datetime.date(int(y), int(m), int(d))
                except ValueError:
                    return '%s-%s-%s' % (y, m, d)
                else:
                    date_value = datetime_safe.new_date(date_value)
                    return date_value.strftime(input_format)
            else:
                return '%s-%s-%s' % (y, m, d)
        return data.get(name, None)

    def create_select(self, name, field, value, val, choices):
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name
        if not (self.required and val):
            choices.insert(0, self.none_value)
        local_attrs = self.build_attrs(id=field % id_)
        s = Select(choices=choices)
        select_html = s.render(field % name, val, local_attrs)
        return select_html

    def _has_changed(self, initial, data):
        try:
            input_format = get_format('DATE_INPUT_FORMATS')[0]
            data = datetime_safe.datetime.strptime(data, input_format).date()
        except (TypeError, ValueError):
            pass
        return super(SelectDateWidget, self)._has_changed(initial, data)
        




class SelectTimeWidget(Widget):
    """
    A Widget that splits time input into <select> elements.
    Allows form to show as 24hr: <hour>:<minute>:<second>, (default)
    or as 12hr: <hour>:<minute>:<second> <am|pm> 
    
    Also allows user-defined increments for minutes/seconds
    """
    hour_field = '%s_hour'
    minute_field = '%s_minute'
    second_field = '%s_second' 
    meridiem_field = '%s_meridiem'
    twelve_hr = False # Default to 24hr.
    
    def __init__(self, attrs=None, hour_step=None, minute_step=15, second_step=15, twelve_hr=False):
        """
        hour_step, minute_step, second_step are optional step values for
        for the range of values for the associated select element
        twelve_hr: If True, forces the output to be in 12-hr format (rather than 24-hr)
        """
        self.attrs = attrs or {}
        
        if twelve_hr:
            self.twelve_hr = True # Do 12hr (rather than 24hr)
            self.meridiem_val = 'a.m.' # Default to Morning (A.M.)
        
        if hour_step and twelve_hr:
            self.hours = range(1,13,hour_step) 
        elif hour_step: # 24hr, with stepping.
            self.hours = range(0,24,hour_step)
        elif twelve_hr: # 12hr, no stepping
            self.hours = range(1,13)
        else: # 24hr, no stepping
            self.hours = range(0,24) 

        if minute_step:
            self.minutes = range(0,60,minute_step)
        else:
            self.minutes = range(0,60)

        if second_step:
            self.seconds = range(0,60,second_step)
        else:
            self.seconds = range(0,60)

    def render(self, name, value, attrs=None):
        try: # try to get time values from a datetime.time object (value)
            hour_val, minute_val, second_val = value.hour, value.minute, value.second
            if self.twelve_hr:
                if hour_val >= 12:
                    self.meridiem_val = 'p.m.'
                else:
                    self.meridiem_val = 'a.m.'
        except AttributeError:
            hour_val = minute_val = second_val = 0
            if isinstance(value, basestring):
                match = RE_TIME.match(value)
                if match:
                    time_groups = match.groups();
                    hour_val = int(time_groups[HOURS]) % 24 # force to range(0-24)
                    minute_val = int(time_groups[MINUTES]) 
                    if time_groups[SECONDS] is None:
                        second_val = 0
                    else:
                        second_val = int(time_groups[SECONDS])
                    
                    # check to see if meridiem was passed in
                    if time_groups[MERIDIEM] is not None:
                        self.meridiem_val = time_groups[MERIDIEM]
                    else: # otherwise, set the meridiem based on the time
                        if self.twelve_hr:
                            if hour_val >= 12:
                                self.meridiem_val = 'p.m.'
                            else:
                                self.meridiem_val = 'a.m.'
                        else:
                            self.meridiem_val = None
                    

        # If we're doing a 12-hr clock, there will be a meridiem value, so make sure the
        # hours get printed correctly
        if self.twelve_hr and self.meridiem_val:
            if self.meridiem_val.lower().startswith('p') and hour_val > 12 and hour_val < 24:
                hour_val = hour_val % 12
        elif hour_val == 0:
            hour_val = 12
            
        output = []
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        # For times to get displayed correctly, the values MUST be converted to unicode
        # When Select builds a list of options, it checks against Unicode values
        hour_val = u"%.2d" % hour_val
        minute_val = u"%.2d" % minute_val
        second_val = u"%.2d" % second_val

        hour_choices = [("%.2d"%i, "%.2d"%i) for i in self.hours]
        local_attrs = self.build_attrs(id=self.hour_field % id_)
        select_html = Select(choices=hour_choices).render(self.hour_field % name, hour_val, local_attrs)
        output.append(select_html)

        minute_choices = [("%.2d"%i, "%.2d"%i) for i in self.minutes]
        local_attrs['id'] = self.minute_field % id_
        select_html = Select(choices=minute_choices).render(self.minute_field % name, minute_val, local_attrs)
        output.append(select_html)

        second_choices = [("%.2d"%i, "%.2d"%i) for i in self.seconds]
        local_attrs['id'] = self.second_field % id_
        select_html = Select(choices=second_choices).render(self.second_field % name, second_val, local_attrs)
        output.append(select_html)
    
        if self.twelve_hr:
            #  If we were given an initial value, make sure the correct meridiem gets selected.
            if self.meridiem_val is not None and  self.meridiem_val.startswith('p'):
                    meridiem_choices = [('p.m.','p.m.'), ('a.m.','a.m.')]
            else:
                meridiem_choices = [('a.m.','a.m.'), ('p.m.','p.m.')]

            local_attrs['id'] = local_attrs['id'] = self.meridiem_field % id_
            select_html = Select(choices=meridiem_choices).render(self.meridiem_field % name, self.meridiem_val, local_attrs)
            output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_hour' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        # if there's not h:m:s data, assume zero:
        h = data.get(self.hour_field % name, 0) # hour
        m = data.get(self.minute_field % name, 0) # minute 
        s = data.get(self.second_field % name, 0) # second

        meridiem = data.get(self.meridiem_field % name, None)

        #NOTE: if meridiem is None, assume 24-hr
        if meridiem is not None:
            if meridiem.lower().startswith('p') and int(h) != 12:
                h = (int(h)+12)%24 
            elif meridiem.lower().startswith('a') and int(h) == 12:
                h = 0
        
        if (int(h) == 0 or h) and m and s:
            return '%s:%s:%s' % (h, m, s)

        return data.get(name, None)
        
# class AdminDateWidget(forms.DateInput):

    # @property
    # def media(self):
        # js = ["admin/js/calendar.js", "admin/js/DateTimeShortcuts.js"]
        # return forms.Media(js=[mymedia("admin/js/%s" % path) for path in js])

    # def __init__(self, attrs=None, format=None):
        # final_attrs = {'class': 'vDateField', 'size': '10'}
        # if attrs is not None:
            # final_attrs.update(attrs)
        # super(AdminDateWidget, self).__init__(attrs=final_attrs, format=format)

