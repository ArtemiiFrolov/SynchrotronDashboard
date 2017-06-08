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
@require_GET
def application_form_view(request):
    if request.method == "POST":
        new_app = Application()
        # Split request creation in two parts
        new_app.station = Station.objects.get(name=request.POST['station'])
        new_app.name = request.POST['name']
        new_app.author = User.objects.get(name=request.POST['author'])

        # TODO: add multiple organizations
        new_app.serial = str(datetime.today().year)+"-"+str(Application.objects.filter(station=new_app.station).count() + 1) + "-" + new_app.station.short_description
        new_app.description = request.POST['description']
        new_app.time_needed = request.POST['time_needed']
        new_app.date_start = request.POST['date_start']
        new_app.date_end = request.POST['date_end']
        new_app.time_start = request.POST['time_start']
        new_app.time_end = request.POST['time_end']
        new_app.complete_status = CompleteStatus.objects.get(name="На рассмотрении")
        new_app.stage_status = StageStatus.objects.get(name="Не принят в работу")

        # how to add multiple?
        new_app.save()
        new_app.organizations.add(Organization.objects.get(name=request.POST['organization']))
        new_app.approaches.add(Approach.objects.get(name=request.POST['metodic']))
        new_app.participants.add(User.objects.get(name=request.POST['participant']))
        new_app.equipment.add(Equipment.objects.get(name=request.POST['equip']))
        context = {'applications': Application.objects.all}
        return render(request, 'applications.html', context)
    else:
        context = {'organizations': Organization.objects.all, 'stations': Station.objects.all, 'metodics': Approach.objects.all, 'participants': User.objects.all, 'equipment': Equipment.objects.all}
        return render(request, 'application_form.html', context)


def application_view(request, request_serial):
    app = get_object_or_404(Application, serial=request_serial)
    return render(request, 'application.html', {'application': app})


def applications_view(request):
    return render(request, 'applications.html', {'applications': Application.objects.all})


def users_view(request):
    context = {'show_users': User.objects.all}
    return render(request, 'users.html', context)


def user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user.html', {'user': user})


def station_view(request, station_short):
    station = get_object_or_404(Station, short_description=station_short)
    return render(request, 'station.html', {'station': station})



