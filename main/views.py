# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_http_methods
from main.models import *
import datetime


def context_processor(request):
    return {
        'foo': 'bar'
    }


@login_required
def index(request):
    return render(request, 'index.html', {})


@require_GET
def test_view(request):
    return render(request, 'test.html', {})


@csrf_protect
@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {})
    if request.method == 'POST':
        user = request.user
        email = request.POST.get('email', "")
        password = request.POST.get('password', "")
        if not user.is_authenticated:
            user = authenticate(username=email, password=password)
            if user is None:
                return redirect(login_view)
            login(request, user)
        return redirect(index)


@login_required
def logout_view(request):
    logout(request)
    return redirect(login_view)


@login_required
@require_http_methods(['GET', 'POST'])
def application_edit(request, serial=None):
    if serial is not None:
        # TODO: make station field unedit
        app = get_object_or_404(Application, serial=serial)
    else:
        app = None

    if request.method == "POST":
        if not app:
            app = Application()
        # Split request creation in two parts
        # TODO: добавить проверку
        app_counter = ApplicationCounter.objects.get(year=datetime.date.today().year)
        station_list = request.POST.getlist('station')
        for station_item in station_list:
            app.station = Station.objects.get(name=station_item)
            app.name = request.POST['name']
            app.author = User.objects.get(name=request.POST['author'])
            app.serial = '%s-%s-%s' % (str(datetime.datetime.today().year),
                                       str(app_counter.number),
                                       app.station.short_description)
            app.description = request.POST['description']
            app.time_needed = request.POST['time_needed']
            app.date_start = request.POST['date_start']
            app.date_end = request.POST['date_end']
            app.time_start = request.POST['time_start']
            app.time_end = request.POST['time_end']
            app.complete_status = CompleteStatus.objects.get_or_create(name="На рассмотрении")
            app.stage_status = StageStatus.objects.get_or_create(name="Не принят в работу")
            # how to add multiple?
            app.save()
            # TODO: need to check, is it ok, or it can be done better way
            organizations_list = request.POST.getlist('organizations')
            for organizations_item in organizations_list:
                app.organizations.add(Organization.objects.get(name=organizations_item))
            approaches_list = request.POST.getlist('approaches')
            for approaches_item in approaches_list:
                app.approaches.add(Approach.objects.get(name=approaches_item))
            # TODO: change output method of participants - it will be too much of chosen objects
            participants_list = request.POST.getlist('participants')
            for participants_item in participants_list:
                app.participants.add(User.objects.get(name=participants_item))
            equipment_list = request.POST.getlist('equipment')
            for equipment_item in equipment_list:
                app.equipment.add(Equipment.objects.get(name=equipment_item))
            app = Application()
        app_counter.number = app_counter.number + 1
        app_counter.save()
        context = {'applications': Application.objects.all}
        return render(request, 'applications.html', context)
    else:
        context = {
            'application': app,
            'organizations': Organization.objects.all,
            'stations': Station.objects.all,
            'approaches': Approach.objects.all,
            'participants': User.objects.all,
            'equipment': Equipment.objects.all}
        return render(request, 'application_form.html', context)


def application_view(request, serial):
    app = get_object_or_404(Application, serial=serial)
    return render(request, 'application.html', {'application': app})


def applications_view(request):
    return render(request, 'applications.html', {'applications': Application.objects.all})


def users_view(request):
    context = {'show_users': User.objects.all}
    return render(request, 'users.html', context)


def user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user.html', {'user': user})


def station_view(request, pk):
    station = get_object_or_404(Station, pk=pk)
    return render(request, 'station.html', {'station': station})


def organization_view(request, pk):
    organization = get_object_or_404(Organization, pk=pk)
    return render(request, 'organization.html', {'organization': organization})

