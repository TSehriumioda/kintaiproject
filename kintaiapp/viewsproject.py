from django.http import HttpResponse
from django.shortcuts import render ,redirect
from .models import TMembers,MDayoff,MProject,TProjtctMembers
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils import timezone
import datetime
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

####
#プロジェクト新規追加
####

def projectcreatefunc(request):
    project_members = {
        'projectmembers_list':TMembers.objects.all()
    }
    return render(request,'projectcreate.html',project_members)

####
#プロジェクト削除
####

def projectdeletefunc(request):
    if request.method == 'POST':
        project_Id = request.POST['project_Id']
        delete_Flg = request.POST['delete_Flg']

        try:
            deleteproject = MProject.objects.get(pk = project_Id)
            deletePmember = TProjtctMembers.objects.filter(pk = project_Id)
            print(deletePmember)
            if delete_Flg == "1":
                if deleteproject.delete_flg is 0:
                    deleteproject.delete_flg = 1

                    print(1)
                    delPM =[]
                    print(2)

                    #TODO:１複数更新ができるようにしたい

                    # TProjtctMembers.objects.filter(pk=project_Id).update(delete_flg=1)

                    for some in deletePmember:
                        some.delete_flg = 1
                        some.save()

                    # for PM in deletePmember:
                    #     PM.delete_flg = 1
                    #     delPM.append(PM)
                    print(3)
                    # TProjtctMembers.objects.bulk_update(delPM, fields=['delete_flg'])
                    deleteproject.save()
                    message = {'message':'削除しました'}
                else:
                    print(deletePmember)
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