from django.shortcuts import render
from django import template
from django.http import HttpResponse
from django.template import RequestContext, loader
from .training import TrainingDay
from .forms import TrainingForm
from datetime import datetime, timedelta


def schedule(request):
    if request.method == 'GET':
        form = TrainingForm(request.GET)
        print(form)
        if form.is_valid():
            short_run1 = request.GET['short_run1']
            short_run2 = request.GET['short_run2']
            rest1 = request.GET['rest1']
            rest2 = request.GET['rest2']
            medium_run = request.GET['medium_run']
            long_run = request.GET['long_run']
            cross_train = request.GET['cross_train']
            race_date = datetime.strptime(request.GET['date'], '%m/%d/%Y')
            training_dict = marathon_schedule(race_date, short_run1, short_run2, rest1, rest2, medium_run, long_run, cross_train)
            context = {
                       'Monday': training_dict['Monday'],
                       'Tuesday': training_dict['Tuesday'],
                       'Wednesday': training_dict['Wednesday'],
                       'Thursday': training_dict['Thursday'],
                       'Friday': training_dict['Friday'],
                       'Saturday': training_dict['Saturday'],
                       'Sunday': training_dict['Sunday'],
                       'range': range(18)
                      }
            return render(request, 'schedule.html', context)
        else:
            return render(request, 'date.html')


def date(request):
    return render(request, 'date.html')


def datetime_range(race_day, weeks):
    weeks -= 1
    start = race_day - timedelta(weeks=weeks, days=(race_day.weekday()))
    span = (race_day + timedelta(days=1)) - start
    for i in range(span.days):
        yield start + timedelta(days=i)


def marathon_schedule(race_day, short_run1, short_run2, rest1, rest2, medium_run, long_run, cross_train):
    """creates a list of Training Day objects"""
    long_run_gen, short_run_gen1, short_run_gen2, medium_run_gen, training_generator = training_generators(race_day)
    training_dict = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 'Thursday':[], 'Friday':[], 'Saturday':[], 'Sunday':[]}
    for date in training_generator:
        weekday = date.strftime("%A")
        if date == (race_day - timedelta(days=1)) or date == (race_day - timedelta(days=2)):
            rest_day = TrainingDay(date, "Rest")
            training_dict[rest_day.weekday_name].append(rest_day)
        if date == race_day:
            race_date = TrainingDay(date, 26.2)
            training_dict[race_date.weekday_name].append(race_date)
            break
        if weekday == short_run1:
            training_dict[short_run1].append(TrainingDay(date, short_run_gen1.__next__()))
        if weekday == rest1:
            training_dict[rest1].append(TrainingDay(date, "Rest"))
        if weekday == medium_run:
            training_dict[medium_run].append(TrainingDay(date, medium_run_gen.__next__()))
        if weekday == short_run2:
            training_dict[short_run2].append(TrainingDay(date, short_run_gen2.__next__()))
        if weekday == rest2:
            training_dict[rest2].append(TrainingDay(date, "Rest"))
        if weekday == long_run:
            training_dict[long_run].append(TrainingDay(date, long_run_gen.__next__()))
        if weekday == cross_train:
            training_dict[cross_train].append(TrainingDay(date, "Cross \nTrain"))
    return training_dict


def training_generators(race_day):
    """creates generators for each weekly run"""
    short_run = [3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 4, 3, 3, None]
    medium_run = [5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 5, 8, 5, 4, 3, 2, 2, None]
    long_run = [5, 6, 7, 8, 10, 11, 12, 14, 16, 16, 17, 18, 19, 20, 22, 9, 8, 8, None]
    long_run_gen = list_generator(long_run)
    short_run_gen1 = list_generator(short_run)
    short_run_gen2 = list_generator(short_run)
    medium_run_gen = list_generator(medium_run)
    training_generator = datetime_range(race_day, 18)
    return long_run_gen, short_run_gen1, short_run_gen2, medium_run_gen, training_generator


def list_generator(input_list):
    for i in input_list:
        yield i

