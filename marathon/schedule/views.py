from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .training import TrainingDay

# Create your views here.

from datetime import datetime, timedelta

def datetime_range(race_day, weeks):
    start = (race_day - timedelta(weeks=weeks)) + timedelta(days=1)
    span = (race_day + timedelta(days=1)) - start
    for i in range(span.days):
        yield start + timedelta(days=i)

def list_generator(input_list):
    for i in input_list:
        yield i


def marathon_schedule(race_day):
    short_run = [3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 4, 3]
    medium_run = [5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 5, 8, 5, 4, 3, 2]
    long_run = [5, 6, 7, 8, 10, 11, 12, 14, 16, 16, 17, 18, 19, 20, 22, 9, 8, 26.2]
    long_run_gen = list_generator(long_run)
    short_run_gen1 = list_generator(short_run)
    short_run_gen2 = list_generator(short_run)
    medium_run_gen = list_generator(medium_run)
    training_generator = datetime_range(race_day, 18)
    training_list = []
    for date in training_generator:
        weekday = date.weekday()
        if weekday == 0:
            training_list.append(TrainingDay(date, short_run_gen1.__next__()))
        if weekday == 1:
            training_list.append(TrainingDay(date, "Rest"))
        if weekday == 2:
            training_list.append(TrainingDay(date, medium_run_gen.__next__()))
        if weekday == 3:
            training_list.append(TrainingDay(date, short_run_gen2.__next__()))
        if weekday == 4:
            training_list.append(TrainingDay(date, "Rest"))
        if weekday == 5:
            training_list.append(TrainingDay(date, long_run_gen.__next__()))
        if weekday == 6:
            training_list.append(TrainingDay(date, "Yoga"))
    return training_list


def index(request):
    race_day = datetime.now()
    training_list = marathon_schedule(race_day)
    for day in training_list:
        print(day)
    context = { 'training_list': training_list }
    return render(request, 'index.html', context)