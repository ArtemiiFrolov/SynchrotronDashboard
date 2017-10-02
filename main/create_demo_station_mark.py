# -*- coding: utf-8 -*-

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard.settings.dev")
django.setup()

from main.models import StationMark, StationMarkValue


def linear_func(x):
    k = 1
    b = 0
    return k*x + b


def square_func(x):
    a = -90
    b = 0
    c = 0
    return a*(x**2) + b*x + c


def sqrt_func(x):
    if x < 0:
        return None
    else:
        return x**1/2


def make_ten_points(mark_name, distrib_law):
    mark, _ = StationMark.objects.get_or_create(name=mark_name)

    StationMarkValue.objects.filter(mark=mark).delete()

    for i in range(0, 10):
        v = StationMarkValue.objects.create(mark=mark, value=float(distrib_law(i)))
        v.save()

if __name__ == '__main__':

    make_ten_points("test1", square_func)
    print('created successfully')
