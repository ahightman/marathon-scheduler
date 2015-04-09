from django import forms

class RaceDayForm(forms.Form):
    race_day = forms.DateField