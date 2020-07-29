from django.http import HttpResponse
from django.shortcuts import render ,redirect
from .models import TMembers,MDayoff,MProject,TProjectMembers
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils import timezone
import datetime
from django.db.models import Max
##########################################
###プロジェクト情報管理画面 使用DB(model)MProject - TProjectMembers
###一覧 新規追加　削除
##########################################

####
#一覧閲覧
####
def projectallfunc(request):
    context = {
        'project_list':MProject.objects.filter(delete_flg = 0)
    }

    return render(request, 'projectall.html',context)

####
#プロジェクト新規追加
####
def projectcreatefunc(request):
    if request.method == 'POST':
        #プロジェクトを作成する       
        project_Id = MProject.objects.all().count()
        project_Id2 =project_Id+1
        project_Code = request.POST['project_Code']
        project_Name = request.POST['project_Name']
        project_Start = request.POST['project_Start']
        project_End = request.POST['project_End']
        dt_now = datetime.datetime.now()

        newproject = MProject.objects.create(project_id=project_Id2,project_name = project_Name,project_code=project_Code,
                                            project_start=project_Start,project_end=project_End,
                                            create_date = dt_now,create_by = 1 ,update_date=dt_now,update_by = 1,delete_flg=0)

        newproject.save()
        
        #プロジェクトメンバーを登録する

        project_Member = request.POST.getlist('s2')

        for item in project_Member:
            TProjectMembers.objects.create(project_id=project_Id2,members_id=item,
                                            create_date = dt_now,create_by = 1 ,
                                            update_date=dt_now,update_by = 1,delete_flg=0)

        project_members = {
            'projectmembers_list':TMembers.objects.all()
        }
        return render(request,'projectcreate.html',project_members)

    else:    
        project_members = {
            'projectmembers_list':TMembers.objects.all()
        }

        return render(request,'projectcreate.html',project_members)

####
#プロジェクト更新
####
def projectupdatefunc(request):


    
    return render(request,'projectupdate.html')

####
#プロジェクト削除
####
def projectdeletefunc(request):
    if request.method == 'POST':
        project_Id = request.POST['project_Id']
        delete_Flg = request.POST['delete_Flg']

        try:
            deleteproject = MProject.objects.get(pk = project_Id)
            if delete_Flg == "1":
                if deleteproject.delete_flg is 0:
                    deleteproject.delete_flg = 1

                    TProjectMembers.objects.filter(pk=project_Id).update(delete_flg=1)

                    deleteproject.save()
                    message = {'message':'削除しました'}
                else:
                    message = {'message':'入力されたデータはすでに削除されています'}
                
                return render(request,'projectdelete.html',message)

            else:
                message = {'message':'削除キャンセルしました'}
                return render(request,'projectdelete.html',message)

        except:
            error = {'error':'入力されたデータは登録されていません'}
            return render(request,'projectdelete.html',error)    

    else:
        return render(request,'projectdelete.html')