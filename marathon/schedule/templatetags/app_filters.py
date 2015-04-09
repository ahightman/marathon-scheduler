from django import template

register = template.Library()

@register.filter
def return_item(l, i):
    try:
        return l[i]
    except:
        return None

@register.filter
def return_weekday(l, i):
    try:
        return l[i].weekday_name
    except:
        return None

@register.filter
def return_run(l, i):
    try:
        return l[i].run
    except IndexError:
        return ""

@register.filter
def return_date(l, i):
    try:
        return l[i].formatted_date
    except IndexError:
        return ""

@register.filter
def plus_one(i):
    return i + 1
