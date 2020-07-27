from django.http import HttpResponse
from django.shortcuts import render ,redirect
from .models import TMembers,MDayoff,MProject
from django.utils import timezone
import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

##########################################
###プロジェクト情報管理画面 使用DB(model)MProject - TProjtctMembers
###一覧
##########################################

####
#一覧閲覧
####
def projectallfunc(request):
    context = {
        'project_list':MProject.objects.filter(delete_flg = 0)
    }
    return render(request, 'projectall.html',context)

