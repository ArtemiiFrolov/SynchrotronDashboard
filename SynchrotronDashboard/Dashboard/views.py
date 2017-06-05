from django.http import HttpResponse
from .models import Organization, Request, Station, Metodic,Right,Role,User,Equipment,CompleteStatus,StageStatus,JournalStatus, EventsList,PlaningExperiment,Experiment,Event,Comment
from django.shortcuts import render
from datetime import date,datetime

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def show_all_users(request):
	context={'show_users':User.objects.all}
	return render(request,'dashboard/show_all_users.html',context)

def create_request(request):
#добавить проверки!!!!!!
    if request.method=="POST":
        new_request=Request()
        #когда пойму как сделать несколько станций - сделать разделение заявки на две части
        new_request.station=Station.objects.get(name=request.POST['station'])
        new_request.name= request.POST['name']
        new_request.author=User.objects.get(name=request.POST['author'])
        #как добавить несколько организаций?
         
        new_request.serial=str(datetime.today().year)+"-"+str(Request.objects.filter(station=new_request.station).count()+1)+"-"+new_request.station.short_description
        new_request.description=request.POST['description']
        new_request.time_needed=request.POST['time_needed']
        new_request.date_start=request.POST['date_start']
        new_request.date_end=request.POST['date_end']
        new_request.time_start=request.POST['time_start']
        new_request.time_end=request.POST['time_end']
        new_request.complete_status=CompleteStatus.objects.get(name="На рассмотрении")
        new_request.stage_status=StageStatus.objects.get(name="Не принят в работу")
         #как добавить несколько ?
        new_request.save()
        new_request.organizations.add(Organization.objects.get(name=request.POST['organization'])) 
        new_request.metodic.add(Metodic.objects.get(name=request.POST['metodic']))
        new_request.participant.add(User.objects.get(name=request.POST['participant']))
        new_request.equipment.add(Equipment.objects.get(name=request.POST['equip']))     
        context={'all_request': Request.objects.all}
        return render(request,'dashboard/show_all_requests.html',context)
    else:
        context={'organizations':Organization.objects.all, 'stations': Station.objects.all, 'metodics': Metodic.objects.all, 'participants': User.objects.all, 'equipment': Equipment.objects.all}
        return render(request,'dashboard/create_request.html',context)

def show_request(request, request_serial):
    if Request.objects.filter(serial=request_serial).exists():
        show_request=Request.objects.get(serial=request_serial)
        context={'show_request': show_request}
        return render(request, 'dashboard/show_request.html', context)
    else:
        return HttpResponse("Такой заявки не существует")
    
def show_user(request, user_id):
    if User.objects.filter(id=user_id).exists():
        show_user=User.objects.get(id=user_id)
        context={'show_user': show_user}
        return render(request, 'dashboard/show_user.html', context)
    else:
        return HttpResponse("Такого пользователя не существует")
        
def show_station(request, station_short):
    if Station.objects.filter(short_description=station_short).exists():
        show_station=Station.objects.get(short_description=station_short)
        context={'show_station': show_station}
        return render(request, 'dashboard/show_station.html', context)
    else:
        return HttpResponse("Такой станции не существует")
        
def show_all_requests(request):
    context={'all_request': Request.objects.all}
    return render(request,'dashboard/show_all_requests.html',context)