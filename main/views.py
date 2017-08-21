# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_http_methods
from main.models import *
import datetime
from django.utils import timezone


def context_processor(request):
    return {
        'foo': 'bar'
    }


@login_required
def index(request):
    return redirect(applications_view)


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
def applications_table(request):
    applications = Application.objects.all()
    if not request.user.has_perm('main.view_application'):
        applications_selected = []
        for application in applications:
            if request.user.has_perm('main.view_application', application) or application.author == request.user or \
                            request.user in application.participants.all():
                if application.pk not in applications_selected:
                    applications_selected.append(application.pk)
            if request.user.has_perm('main.view_station_application', application.station) or application.station in request.user.station.all():
                if application.pk not in applications_selected:
                    applications_selected.append(application.pk)
        applications = Application.objects.filter(pk__in=applications_selected)

    filtered = 'all'
    if request.GET.get('filter'):
        filtered = request.GET.get('filter')
    if filtered == 'consideration':
        applications = applications.filter(stage_status__name="На рассмотрении")
    if filtered == 'accepted':
        applications = applications.filter(stage_status__name="Заявка принята")
    if filtered == 'returned':
        applications = applications.filter(stage_status__name="Возвращена с комментариями")
    if filtered == 'disapproved':
        applications = applications.filter(stage_status__name="Заявка отклонена")
    if filtered == 'finished':
        applications = applications.filter(stage_status__name="Завершенные")
    if request.GET.get('my', None):
        applications = applications.filter(author__pk=request.user.pk)
    if request.GET.get('part', None):
        applications = applications.filter(participants__pk=request.user.pk)
    return render(request, 'include/applications_list.html', {'applications': applications})


def application_row(request, pk):
    app = Application.objects.get(pk=pk)
    can_edit = False
    can_return = False
    can_approve = False
    can_decline = False
    if request.user.has_perm('edit_applications') or request.user.has_perm('edit_applications', app) or request.user == app.author:
        can_edit = True
    if request.user.has_perm('approve_applications') or request.user.has_perm('approve_applications', app):
        can_approve = True
    if request.user.has_perm('decline_applications') or request.user.has_perm('decline_applications', app):
        can_decline = True
    if request.user.has_perm('return_applications') or request.user.has_perm('return_applications', app):
        can_return = True
    for station in Station.objects.all():
        if request.user.has_perm('edit_station_application') or request.user.has_perm('edit_station_application', station):
            can_edit = True
        if request.user.has_perm('approve_station_application') or request.user.has_perm('approve_station_application', station):
            can_approve = True
        if request.user.has_perm('decline_station_application') or request.user.has_perm('decline_station_application', station):
            can_decline = True
        if request.user.has_perm('return_station_application') or request.user.has_perm('return_station_application', station):
            can_return = True
    app.stage_status = StageStatus.objects.get_or_create(name='Заявка принята')
    app.save()
    return render(request, 'include/application_row.html', {'application': get_object_or_404(Application, pk=pk),
                                                            'can_edit': can_edit,
                                                            'can_return': can_return,
                                                            'can_approve': can_approve,
                                                            'can_decline': can_decline})


def application_row_disapprove(request, pk):
    app = Application.objects.get(pk=pk)
    can_decline = False
    if request.user.has_perm('decline_applications') or request.user.has_perm('decline_applications', app):
        can_decline = True
    for station in Station.objects.all():
        if request.user.has_perm('decline_station_application') or request.user.has_perm('decline_station_application', station):
            can_decline = True
    if can_decline:
        app.stage_status = StageStatus.objects.get_or_create(name='Заявка отклонена')
    app.save()
    return render(request, 'include/application_row.html', {'application': get_object_or_404(Application, pk=pk)})


def modal_show(request, pk):
    return render(request, 'include/modal.html', {'application': get_object_or_404(Application, pk=pk)})


def comment_from_application(request, pk):
    app = get_object_or_404(Application, pk=pk)
    if request.method == "POST":
        if 'Return' in request.POST:
            app.stage_status = StageStatus.objects.get_or_create(name='Возвращена с комментариями')
            app.save()
        comment = Comment()
        comment.application = app
        comment.author = User.objects.get(name=request.user.name)
        comment.text = request.POST['description']
        comment.save()
    return redirect(application_view, serial=app.serial)


def comment_from_modal(request, pk):
    app = get_object_or_404(Application, pk=pk)
    if request.method == "POST":
        if 'Return' in request.POST:
            app.stage_status = StageStatus.objects.get_or_create(name='Возвращена с комментариями')
            app.save()
        comment = Comment()
        comment.application = app
        comment.author = User.objects.get(name=request.user.name)
        comment.text = request.POST['description']
        comment.save()
    return redirect(applications_view)


@login_required
@require_http_methods(['GET', 'POST'])
def application_edit(request, serial=None):
    if serial is not None:
        # TODO: make station field unedit
        app = get_object_or_404(Application, serial=serial)
    else:
        app = None

    if request.method == "POST":
        context = {}
        errors = {}
        if not app:
            app = Application()
        context['application'] = app
        # Split request creation in two parts
        # TODO: добавить проверку
        app_counter = ApplicationCounter.objects.get(year=timezone.now().year)
        station_list = request.POST.getlist('station')
        for station_item in station_list:
            app.station = Station.objects.get(id=station_item)
            app.name = request.POST['name']
            app.author = User.objects.get(id=request.POST['author'])
            if not app.serial:
                app.serial = '%s-%s-%s' % (str(timezone.now().year),
                                           str(app_counter.number),
                                           app.station.short_description)
            app.description = request.POST['description']
            app.time_needed = request.POST['time_needed']
            app.start = datetime.datetime.strptime(request.POST['start'], "%d.%m.%Y %H:%M")
            app.end = datetime.datetime.strptime(request.POST['end'], "%d.%m.%Y %H:%M")
            app.complete_status = CompleteStatus.objects.get_or_create(name="На рассмотрении")
            app.stage_status = StageStatus.objects.get_or_create(name="На рассмотрении")
            if not errors:
                app.save()
            else:
                context['errors'] = errors
                render(request, 'application_form.html', context)
            # TODO: need to check, is it ok, or it can be done better way
            organizations_list = request.POST.getlist('organizations')
            for organizations_item in organizations_list:
                try:
                    Organization.objects.get(id=organizations_item)
                except Exception:
                    app.organizations.add(Organization.objects.get_or_create(name=organizations_item))
                else:
                    app.organizations.add(Organization.objects.get(id=organizations_item))
            approaches_list = request.POST.getlist('approaches')
            for approaches_item in approaches_list:
                try:
                    Approach.objects.get(id=approaches_item)
                except Exception:
                    app.approaches.add(Approach.objects.get_or_create(name=approaches_item))
                else:
                    app.approaches.add(Approach.objects.get(id=approaches_item))
            # TODO: change output method of participants - it will be too much of chosen objects
            participants_list = request.POST.getlist('participants')
            for participants_item in participants_list:
                try:
                    User.objects.get(id=participants_item)
                except Exception:
                    app.participants.add(User.objects.get_or_create(name=participants_item))
                else:
                    app.participants.add(User.objects.get(id=participants_item))
            equipment_list = request.POST.getlist('equipment')
            for equipment_item in equipment_list:
                app.equipment.add(Equipment.objects.get(id=equipment_item))
            app = Application()
        app_counter.number = app_counter.number + 1
        app_counter.save()

        return redirect(applications_view)
    else:
        context = {
            'application': app,
            }
        return render(request, 'application_form.html', context)

#
# def application_approve(request, serial):
#     if ...:
#
#     return redirect(application_view, serial=serial)


def application_view(request, serial):
    app = get_object_or_404(Application, serial=serial)
    return render(request, 'application.html', {'application': app})


def applications_view(request):
    applications = Application.objects.all()
    filtered = 'all'
    if request.GET.get('filter'):
        filtered = request.GET.get('filter')
    return render(request, 'applications.html', {'applications': applications, 'filtered': filtered})


def all_users(request):
    context = {'users': User.objects.all, 'stations': Station.objects.all, 'organizations': Organization.objects.all}
    return render(request, 'all_users.html', context)


def user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user.html', {'user': user})


def station_view(request, pk):
    station = get_object_or_404(Station, pk=pk)
    return render(request, 'station.html', {'station': station})


def organization_view(request, pk):
    organization = get_object_or_404(Organization, pk=pk)
    return render(request, 'organization.html', {'organization': organization})


# TODO: make without refresh (multiple choices of station)
def planning_experiments(request):
    if request.GET.get('station'):
        station = request.GET.get('station')
        if station == "All":
            context = {'stations': Station.objects.all,
                       'applications': Application.objects.all().filter(stage_status__name='Заявка принята'),
                       'text': "Все станции"}
        else:
            station = Station.objects.get(name=station)
            context = {'stations': Station.objects.all,
                       'applications': Application.objects.all().filter(stage_status__name='Заявка принята',
                                                                        station=station),
                       'text': station.name
                       }
    else:
        context = {'stations': Station.objects.all,
                   'applications': Application.objects.all().filter(stage_status__name='Заявка принята'),
                   'text': "Все станции"}
    return render(request, 'planning_experiments.html', context)


def planned_table(request):
    station = "Все"
    planned_experiments_chosen = ExperimentPlan.objects.all()

    filtered = 'all'
    if request.GET.get('filter'):
        filtered = request.GET.get('filter')
    if filtered == 'finished':
        planned_experiments_chosen = planned_experiments_chosen.filter(status__name="Эксперимент выполнен")
    if filtered == 'unfinished':
        planned_experiments_chosen = planned_experiments_chosen.filter(status__name="Эксперимент не выполнен")
    if request.GET.get('station'):
        station = request.GET.get('station')
    if station != "Все":
        station = Station.objects.get(name=station)
        planned_experiments_chosen = planned_experiments_chosen.filter(station=station)
    return render(request, 'include/planned_experiments_list.html', {'planned_experiments': planned_experiments_chosen})


@login_required
def planned_experiments(request):
    if request.GET.get('station'):
        station = request.GET.get('station')
        if station == "Все":
            context = {'stations': Station.objects.all,
                       'planned_experiments': ExperimentPlan.objects.all(),
                       'text': "Все"}
        else:
            station = Station.objects.get(name=station)
            context = {'stations': Station.objects.all,
                       'planned_experiments': ExperimentPlan.objects.all().filter(station=station),
                       'text': station.name
                       }
    else:
        context = {'stations': Station.objects.all,
                   'planned_experiments': ExperimentPlan.objects.all(),
                   'text': "Все"}
    return render(request, 'planned_experiments.html', context)


def planning_calendar(request):
    if request.GET.get('station'):
        station = request.GET.get('station')
        station = Station.objects.get(name=station)

    else:
        station = Station.objects.first()
    if request.GET.get('application'):
        app = request.GET.get('application')
        app = Application.objects.get(serial=app)
        station = app.station

    else:
        app = Application.objects.first()
    if request.method == "POST":
        explan = ExperimentPlan()
        explan.author = User.objects.get(name=request.user.name)
        explan.application = Application.objects.get(serial=request.POST['serial'])
        explan.start = datetime.datetime.strptime(request.POST['start'], "%d.%m.%Y %H:%M")
        explan.end = datetime.datetime.strptime(request.POST['end'], "%d.%m.%Y %H:%M")
        explan.status = JournalStatus.objects.get_or_create(name='Эксперимент не выполнен')
        explan.station = station
        explan.save()
    context = {'stations': Station.objects.all,
               'applications': Application.objects.all().filter(stage_status__name='Заявка принята',
                                                                station=station),
               'text': station.name,
               'planned_experiments': ExperimentPlan.objects.all().filter(station=station),
               'selected_app': app
               }
    return render(request, 'planning_calendar.html', context)


def journal(request):
    if request.GET.get('station'):
        station = request.GET.get('station')
        if station == "All":
            context = {'stations': Station.objects.all,
                       'experiments': Experiment.objects.all(),
                       'text': "Все станции"}
        else:
            station = Station.objects.get(name=station)
            context = {'stations': Station.objects.all,
                       'experiments': Experiment.objects.all().filter(station=station),
                       'text': station.name
                       }
    else:
        context = {'stations': Station.objects.all,
                   'experiments': Experiment.objects.all(),
                   'text': "Все станции"}
    return render(request, 'journal.html', context)


def journal_new(request):
    if request.GET.get('planned'):
        planned_ex = request.GET.get('planned')
        planned_ex = ExperimentPlan.objects.get(pk=planned_ex)
        flag = True
    else:
        planned_ex = ExperimentPlan.objects.first()
        flag = False
    start_time = planned_ex.start.strftime("%H:%M")
    start_date = planned_ex.start.strftime("%Y-%m-%d")
    end_time = planned_ex.end.strftime("%H:%M")
    end_date = planned_ex.end.strftime("%Y-%m-%d")

    if request.method == "POST":
        experiment = Experiment()
        experiment.author = User.objects.get(name=request.user.name)
        experiment.application = Application.objects.get(serial=request.POST['serial'])
        experiment.start = datetime.datetime.strptime(request.POST['start'], "%d.%m.%Y %H:%M")
        experiment.end = datetime.datetime.strptime(request.POST['end'], "%d.%m.%Y %H:%M")
        experiment.operator = User.objects.get(name=request.POST['operator'])
        experiment.methods = Approach.objects.get(name=request.POST['approach'])
        experiment.comment = request.POST['comment']
        experiment.station = Station.objects.get(name=request.POST['station'])
        experiment.save()
        explan = ExperimentPlan.objects.get(pk=request.POST['ex_plan'])
        if explan.application == experiment.application:
            explan.status = JournalStatus.objects.get_or_create(name='Эксперимент выполнен')
            explan.save()
        return redirect(journal)

    context = {'stations': Station.objects.all,
               'applications': Application.objects.all().filter(stage_status__name='Заявка принята'),
               'methods': Approach.objects.all,
               'users': User.objects.all,
               'planned_experiments': ExperimentPlan.objects.all,
               'planned_ex': planned_ex,
               'start_time': start_time,
               'start_date': start_date,
               'end_time':  end_time,
               'end_date': end_date,
               'flag': flag,
               }
    return render(request, 'journal_new.html', context)


def synchrotron_calendar(request):
    if request.method == "POST":
        event = Event()
        event.name = EventsList.objects.get(pk=request.POST['event'])
        event.start = datetime.datetime.strptime(request.POST['start'], "%d.%m.%Y %H:%M")
        event.end = datetime.datetime.strptime(request.POST['end'], "%d.%m.%Y %H:%M")
        event.save()
    context = {'events': Event.objects.all(),
               'eventsList': EventsList.objects.all(),
               }
    return render(request, 'synchrotron_calendar.html', context)