# -*- coding: utf-8 -*-

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard.settings.dev")
django.setup()

from main.models import StationMark, StationMarkValue


def linear_func(x):
    return x


def square_func(x):
    return x * x


def sqrt_func(x):
    if x < 0:
        return None
    else:
        return x**1/2


def make_ten_points(mark_instance, distrib_law):
    StationMarkValue.objects.filter(mark=mark_instance).delete()

    for i in range(0, 10):
        v = StationMarkValue.objects.create(mark=mark_instance, value=float(distrib_law(i)))
        v.save()

if __name__ == '__main__':
    mark, _ = StationMark.objects.get_or_create(name="test1")
    make_ten_points(mark, square_func)
    print('created successfully')
