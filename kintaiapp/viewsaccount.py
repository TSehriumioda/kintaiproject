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

            loginusername  = TMembers.objects.values_list('members_name',flat=True).get(members_id=members_id2)
            loginuseradmin = TMembers.objects.values_list('admin_flg',flat=True).get(members_id = members_id2)
            request.session['loginmembers_id'] = members_id2
            request.session['loginusername'] = loginusername
            request.session['loginuser'] = loginuseradmin

            name = request.session['loginusername']
            print(name)
            return redirect('eturan')
        except:
            return render(request,'login.html',{'error':'入力されたユーザーは登録されていません'})

    return render(request,'login.html')

def logoutfunc(request):
    del request.session['loginuser']
    del request.session['loginusername']
    request.session.clear()
    request.session.flush()
    return render(request,'login.html',{'error':'ログアウトしました'})