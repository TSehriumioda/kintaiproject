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
    if request.method == 'POST':
        ########## 一覧画面　value=0 ##############
        if request.POST['hiddenpost'] is '0':
            project_Id = request.POST['project_id']
            print(project_Id)

            #プロジェクトコードからデータ取得する
            updateproject = MProject.objects.get(pk=project_Id)
            choosemember = TProjectMembers.objects.filter(pk=project_Id)

            #外部結合ができなくて無理やりつくったので直したい
            choosemembers_list = []
            for cname in choosemember: 
                choosemembers_list.append(cname.members_id)
            print(choosemembers_list)

            member = TMembers.objects.all()
            A_list = []
            B_list =[]
            for it in member:
                if it.members_id not in choosemembers_list:
                    A_list.append(it)
                else:
                    B_list.append(it)

            iru =[]
            for aaaaa in B_list:
                OS = TMembers.objects.get(members_id = aaaaa.members_id)
                iru.append(OS)

            inai =[]
            for vvv in A_list:
                OS = TMembers.objects.get(members_id = vvv.members_id)
                inai.append(OS)
            
            #取得したデータをフォームの中に入れる
            checked = {
                'project_code':updateproject.project_code,
                'project_name':updateproject.project_name,
                'project_Start':updateproject.project_start,
                'project_End':updateproject.project_end,
                'allmember':inai,
                'choosemember':iru,
                'project_id':project_Id,
            }
            return render(request,'projectupdate.html',checked)

        ########## 編集画面　value=１ ##############
        else:
            print("編集画面から")
            project_Id = request.POST['project_id']
            
            project_Code = request.POST['project_Code']
            project_Name = request.POST['project_Name']
            project_Start = request.POST['project_Start']
            project_End = request.POST['project_End']

            create_Date = MProject.objects.values_list('create_date', flat=True).get(pk = project_Id)
            create_By   = MProject.objects.values_list('create_by', flat=True).get(pk = project_Id)
            dt_now = datetime.datetime.now()

            try:
                updateproject = MProject(project_id=project_Id,project_name = project_Name,project_code=project_Code,
                                                    project_start=project_Start,project_end=project_End,
                                                    create_date = create_Date,create_by = create_By ,update_date=dt_now,update_by = 1,delete_flg=0)

                updateproject.save()

                TProjectMembers.objects.filter(pk=project_Id).delete()

                project_Member = request.POST.getlist('s2')

                for item in project_Member:
                    TProjectMembers.objects.update_or_create(project_id=project_Id,members_id=item,
                                                    create_date = dt_now,create_by = 1 ,
                                                    update_date=dt_now,update_by = 1,delete_flg=0)

                project_members = {
                    'projectmembers_list':TMembers.objects.all(),
                    'message':'更新されました',
                     'project_list':MProject.objects.filter(delete_flg = 0)

                }
                return render(request,'projectall.html',project_members)

            except:
                notnewproject = MProject.objects.get(pk = project_Id)
                print("登録されていないプロジェクトです")
                return render(request,'projectupdate.html',{'error':'エラー'})



            return render(request,'projectupdate.html',{'error':'編集画面から'})


    else:
        project_members = {
            'projectmembers_list':TMembers.objects.all()
        }
        return render(request,'projectupdate.html',project_members)


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