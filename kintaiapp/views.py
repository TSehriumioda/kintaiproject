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
###ログイン画面 使用DB(model)TMembes
##########################################

def loginfunc(request):
    if  request.method == 'POST':

        members_id2 = request.POST['members_Id']
        password2 = request.POST['password']

        # if type(members_id2)is not int:
        #     return render(request,'login.html',{'error':'members_Idは半角数字で入力してください'} )
        #名前とパスワードで照合したほうが使いやすいと思うので最終的には変更したい

        try:
            entries = TMembers.objects.get(members_id=members_id2,password=password2)
            return redirect('eturan')
        except:
            return render(request,'login.html',{'error':'入力されたユーザーは登録されていません'})

    return render(request,'login.html')

##########################################
###社員情報管理画面　使用DB(model)TMembers
# 閲覧/追加/更新/削除
##########################################

####
#一覧閲覧
####
def eturanfunc(request):
    context = {
        'members_list':TMembers.objects.all()
    }
    return render(request, 'eturan.html',context)

####
#新規追加
####
def createfunc(request):
    if request.method == 'POST':

        members_Id = request.POST['members_Id']
        members_Name = request.POST['members_Name']
        password = request.POST['password']
        admin_Flg = request.POST['admin_Flg']
        allpayd_Days = request.POST['allpayd_Days']

        dt_now = datetime.datetime.now()
        try:
            member = TMembers.objects.get(members_id = members_Id)
            error = {'error':'このユーザーは登録されています'}
            return render(request, 'eturan.html',error)
        except:
            user = TMembers(members_id = members_Id,members_name = members_Name,password = password,
                            admin_flg = admin_Flg,allpayd_days = int(allpayd_Days),create_date = dt_now,
                            create_by = "仮",update_date=dt_now,update_by = "仮")

            user.save()
            return render(request,'login.html')

    return render(request,'createmembers.html')

####
#更新
####
def updatemembersfunc(request):
    if request.method == 'POST':
        members_Id = request.POST['members_Id']
        members_Name = request.POST['members_Name']
        password = request.POST['password']
        admin_Flg = request.POST['admin_Flg']
        allpayd_Days = request.POST['allpayd_Days']

        create_Date = TMembers.objects.values_list('create_date', flat=True).get(pk = members_Id)
        create_By   = TMembers.objects.values_list('create_by', flat=True).get(pk = members_Id)
        dt_now = datetime.datetime.now()
        user = TMembers(members_id = members_Id,members_name = members_Name,password = password,
                        admin_flg = admin_Flg,allpayd_days = int(allpayd_Days),create_date = create_Date,
                        create_by = create_By,update_date=dt_now,update_by = "仮")

        try:
            member = TMembers.objects.get(members_id = members_Id)
            user.save()
            return render(request,'login.html')
        except:
            error = {'error':'このユーザーは登録されていません'}
            return render(request, 'eturan.html',error)    

    return render(request,'updatemembers.html')

####
#削除
####
def deletemembersfunc(request):
    if request.method == 'POST':
        members_Id = request.POST['members_Id']
        delete_Flg = request.POST['delete_Flg']

        try:
            member = TMembers.objects.get(members_id = members_Id)
            if delete_Flg == "1":
                member.delete()
                message = {'message':'削除しました'}
                print("削除しました")
            else:
                message = {'message':'削除キャンセルしました'}
                print("削除キャンセルしました")
            return render(request,'login.html',message)

        except:
            error = {'error':'このユーザーは登録されていません'}
            return render(request, 'eturan.html',error)    

    return render(request,'deletemembers.html')