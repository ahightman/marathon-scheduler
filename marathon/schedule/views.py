from django.shortcuts import render
from django import template
from django.http import HttpResponse
from django.template import RequestContext, loader
from .training import TrainingDay
from .forms import RaceDayForm
from datetime import datetime, timedelta


def schedule(request):
    if request.method == 'GET':
        race_date = datetime.strptime(request.GET['date'], '%m/%d/%Y')
        print(date)
        training_dict = marathon_schedule(race_date)
        print(training_dict['Monday'])
        context = {
                   'Monday': training_dict['Monday'],
                   'Tuesday': training_dict['Tuesday'],
                   'Wednesday': training_dict['Wednesday'],
                   'Thursday': training_dict['Thursday'],
                   'Friday': training_dict['Friday'],
                   'Saturday': training_dict['Saturday'],
                   'Sunday': training_dict['Sunday'],
                   'range': range(len(training_dict['Sunday']))
                  }
        return render(request, 'schedule.html', context)


def date(request):
    return render(request, 'date.html')


def datetime_range(race_day, weeks):
    start = (race_day - timedelta(weeks=weeks)) + timedelta(days=1)
    span = (race_day + timedelta(days=1)) - start
    for i in range(span.days):
        yield start + timedelta(days=i)


def marathon_schedule(race_day):
    """creates a list of Training Day objects"""
    long_run_gen, short_run_gen1, short_run_gen2, medium_run_gen, training_generator = training_generators(race_day)
    training_dict = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 'Thursday':[], 'Friday':[], 'Saturday':[], 'Sunday':[]}
    for date in training_generator:
        weekday = date.weekday()
        if date == (race_day - timedelta(days=1)) or date == (race_day - timedelta(days=2)):
            rest_day = TrainingDay(date, "Rest")
            training_dict[rest_day.weekday_name].append(rest_day)
        if date == race_day:
            race_date = TrainingDay(date, 26.2)
            training_dict[race_date.weekday_name].append(race_date)
            continue
        if weekday == 0:
            training_dict['Monday'].append(TrainingDay(date, short_run_gen1.__next__()))
        if weekday == 1:
            training_dict['Tuesday'].append(TrainingDay(date, "Rest"))
        if weekday == 2:
            training_dict['Wednesday'].append(TrainingDay(date, medium_run_gen.__next__()))
        if weekday == 3:
            training_dict['Thursday'].append(TrainingDay(date, short_run_gen2.__next__()))
        if weekday == 4:
            training_dict['Friday'].append(TrainingDay(date, "Rest"))
        if weekday == 5:
            training_dict['Saturday'].append(TrainingDay(date, long_run_gen.__next__()))
        if weekday == 6:
            training_dict['Sunday'].append(TrainingDay(date, "Yoga"))
    return training_dict


def training_generators(race_day):
    """creates generators for each weekly run"""
    short_run = [3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 4, 3, 3]
    medium_run = [5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 5, 8, 5, 4, 3, 2, 2]
    long_run = [5, 6, 7, 8, 10, 11, 12, 14, 16, 16, 17, 18, 19, 20, 22, 9, 8, 8]
    long_run_gen = list_generator(long_run)
    short_run_gen1 = list_generator(short_run)
    short_run_gen2 = list_generator(short_run)
    medium_run_gen = list_generator(medium_run)
    training_generator = datetime_range(race_day, 18)
    return long_run_gen, short_run_gen1, short_run_gen2, medium_run_gen, training_generator

def list_generator(input_list):
    for i in input_list:
        yield i

