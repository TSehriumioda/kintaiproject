from django.http import HttpResponse
from django.shortcuts import render ,redirect
from .models import TMembers,MDayoff
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

##########################################
###休暇情報管理画面 使用DB(model)MDayoff - TMembers
###一覧 新規追加
##########################################

####
#一覧閲覧
####
def dayoffallfunc(request):
    context = {
        'dayoff_list':MDayoff.objects.filter(delete_flg = 0)
    }
    return render(request, 'dayoffall.html',context)


####
#新規追加
####
def dayoffcreatefunc(request):
    if request.method == 'POST':

        dayoff_Name = request.POST['dayoff_Name']
        dayoff_Attribute = request.POST['dayoff_attribute']
        work_Time = request.POST['work_time']
        dt_now = datetime.datetime.now()

        newDayoff = MDayoff.objects.create(dayoff_name = dayoff_Name,dayoff_attribute=dayoff_Attribute,work_time = work_Time,
                        create_date = dt_now,create_by = 1 ,update_date=dt_now,update_by = 1)

        newDayoff.save()
        return render(request,'dayoffcreate.html',{'message':'正しく登録されました'})

    return render(request,'dayoffcreate.html')

####
#更新
####
def dayoffupdatefunc(request):
    if request.method == 'POST':

        dayoff_Id   = request.POST['dayoff_Id']
        dayoff_Name = request.POST['dayoff_Name']
        dayoff_Attribute = request.POST['dayoff_attribute']
        work_Time = request.POST['work_time']
        dt_now = datetime.datetime.now()

        create_Date = MDayoff.objects.values_list('create_date', flat=True).get(pk = dayoff_Id)
        create_By   = MDayoff.objects.values_list('create_by', flat=True).get(pk = dayoff_Id)
        dt_now = datetime.datetime.now()


        newDayoff = MDayoff(dayoff_id = dayoff_Id,dayoff_name = dayoff_Name,
                            dayoff_attribute=dayoff_Attribute,work_time = work_Time,
                            create_date = create_Date,create_by = create_By,update_date=dt_now,update_by = 1)

        try:
            dayoff = MDayoff.objects.get(dayoff_id = dayoff_Id)            
            newDayoff.save()
            return render(request,'dayoffupdate.html',{'message':'正しく更新されました'})
        except:
            return render(request, 'dayoffupdate.html',{'error':'この休暇情報は登録されていません'})    

    return render(request,'dayoffupdate.html')

####
#削除
####
