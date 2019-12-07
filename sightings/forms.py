from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _

from .models import Squirrel

class SightingForm(ModelForm):
    class Meta:
        model = Squirrel
        fields = ['latitude', 'longitude', 'squirrel_id', 'shift', 'date', 'age', \
                  'fur_color', 'location', 'specific_location', 'running', \
                  'chasing', 'climbing', 'eating', 'foraging', \
                  'kuks', 'quaas', 'moans', 'tail_flags', 'tail_twitches', \
                  'approaches', 'indifferent', 'runs_from', 'other_activities']

        labels = {
            'latitude': _('Latitude'),
            'longitude': _('Longitude'),
            'fur_color': _('Primary Fur Color'),
            'runs_from': _('Runs away from human'),
            'approaches': _('Approaches human'),
        }

        help_texts = {
            'latitude': None,
            'longitude': None,
            'squirrel_id': None,
            'date': None,
            'specific_location': None,
            'running': None,
            'chasing': None,
            'climbing': None,
            'eating': None,
            'foraging': None,
            'kuks': None,
            'quaas': None,
            'moans': None,
            'tail_flags': None,
            'tail_twitches': None,
            'approaches': None,
            'indifferent': None,
            'runs_from': None,
            'other_activities': None,
            'fur_color': None,
            'location': None,
            'age': None,
            'shift': None,
        }

    date = forms.DateField(
        input_formats=['%Y-%m-%d', ],
        widget=forms.DateInput(attrs={
            'class': 'form-control datepicker-input',
            'type': 'date',
        })
    )

