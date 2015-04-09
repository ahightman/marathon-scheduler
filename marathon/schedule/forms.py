from django import forms

class RaceDayForm(forms.Form):
    race_day = forms.DateField

class TrainingForm(forms.Form):
    short_run1 = forms.CharField()
    short_run2 = forms.CharField()
    rest1 = forms.CharField()
    rest2 = forms.CharField()
    medium_run = forms.CharField()
    long_run = forms.CharField()
    cross_train = forms.CharField()