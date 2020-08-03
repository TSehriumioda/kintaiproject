from django.http import HttpResponse
from django.shortcuts import render ,redirect
from .models import TMembers,MDayoff,TAttendance,TAttendanceDetail,TWorkDetail,MProject
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
import datetime
import calendar
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

def kintaieturanfunc(request):
    #####年月日を返す
    if request.method == 'POST':
        return render(request,'kintaieturan.html')
    else:
        #確定フラグのたっていない月をリスト化して選択できるようにする
        workmonth = TAttendance.objects.values_list('year_month').filter(members_id = 3,confirm_flg=0)
        #当月のカレンダーをつくる
        dt = datetime.date.today()
        year = dt.year
        month = dt.month
        dtyoubi = calendar.monthrange(year,month)[0]
        dtmonth = calendar.monthrange(year,month)[1]

        w_list = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']
        
        # workdate_1 = 1
        # work_id_1 =1
        # projectwtlist = syousai(work_date1=workdate_1,work_id1=work_id_1)

        # times = TAttendanceDetail.objects.get(work_date=1,work=1)
        # print(times.actualwork_time)

        alllist =[]
        #勤怠詳細用のリスト
        # projectwtlist = []

        for days in range(1,dtmonth + 1):
            # days = 日付作成
            #曜日作成
            print("#0")
            print(days)
            today = datetime.datetime(year, month, days)
            a = today.weekday()
            print(today)
            print(a)
            try:
                print(days)
                print("#1")
                # #元になるデータ取得　7/1なら1のデータ
                # A = str(days)
                # print(A)
                projectwtlist = []

                times = TAttendanceDetail.objects.get(work_date = days )

                print("#2")
                #休暇名
                dayoffname =times.dayoff.dayoff_name
                print("#3")
                #出勤時間取得
                start_time = times.start_time.strftime("%H:%M")
                #退勤時間取得
                end_time = times.end_time.strftime("%H:%M")
                #休憩時間取得
                print("#4")
                break_time = times.break_time
                #実働時間取得
                print("#5")
                actual_worktime = times.actualwork_time
                #労働時間取得
                work_time = times.work_time
                print("#6")

                #作業内訳##########################################################################################

                #TODO:work_dateで日付ごとのデータはとりだせてるらしいのでまとめて表示されない方法を調べたい
                workdetailId = TAttendanceDetail.objects.values_list("workdetail_id").get(work_date=days)
                #上で取得したworkdetailIdと同じの、TWorkDetailのworkdetailを持ってきて外部結合させてTWDとする
                # TWD_list = TWorkDetail.objects.select_related().filter(workdetail = workdetailId,)
                TWD_list = TWorkDetail.objects.filter(workdetail = workdetailId)
                print("#7")
                for i in TWD_list:
                    project_id = i.project.project_id
                    pro = MProject.objects.get(project_id=project_id)

                    print(pro)
                    pname = pro.project_name
                    # TWDのworkdetailをもとに各作業時間をTWorkdetaiテーブルから取り出す
                    proworktime = i.workproject_time
                    nameAndworktime={
                        'pname':pname,
                        'pworktime':proworktime
                        }
                    print(nameAndworktime)
                    projectwtlist.append(nameAndworktime)

                print("#8")
                #全項目追加
                alldata = {'day':days,'youbi':w_list[a],'dayoffname':dayoffname,'start_time':start_time,
                            'end_time':end_time,'break_time':break_time,'actual_worktime':actual_worktime,'work_time':work_time,
                            'workdetaillist':projectwtlist}

                alllist.append(alldata)
                print(days)
                print("#9")
                
            except:
                print("##except:##")
                print(days)
                times = ""
                #出勤時間取得
                start_time = ""
                #退勤時間取得
                end_time = ""
                #休憩時間取得
                break_time =  ""
                #実働時間取得
                actual_worktime = ""
                #労働時間取得
                work_time = ""
                #作業内訳
                
                #全項目追加
                alldata = {'day':days,'youbi':w_list[a],'dayoffname':"",'start_time':start_time,
                            'end_time':end_time,'break_time':break_time,'actual_worktime':actual_worktime,'work_time':work_time}
                print(alldata)
                alllist.append(alldata)
                pass

        # # 当月分の勤怠詳細を持ってくる
        # # 当月分の勤怠詳細を計算する→結果を出す

        context={
            'workmonth':workmonth,
            'month':month,
            #現在はwork_date=1、work_id=1のもののみ テストデータ入れたらfor文の中に一緒に入れる
            # 'workdetail':projectwtlist,
            'alllist':alllist,
        }
        return render(request,'kintaieturan.html',context)

def syousai(work_date1,work_id1):
    #作業内訳を取得してまとめる
    #1日のworkdetail_idをTAttendanceDetailから取得する work_dateは稼働日、work_idは年月
    workdetailId = TAttendanceDetail.objects.values_list("workdetail_id").get(work_date=work_date1,work_id=work_id1)
    #上で取得したworkdetailIdと同じの、TWorkDetailのworkdetailを持ってきて外部結合させてTWDとする
    TWD = TWorkDetail.objects.select_related().filter(workdetail = workdetailId)
    # TWDのworkdetailをもとにプロジェクト名を出す
    projectwtlist = []

    for i in TWD:
        project_id = i.project.project_id
        pro = MProject.objects.get(project_id=project_id)
        pname = pro.project_name
    #TWDのworkdetailをもとに各作業時間をTWorkdetaiテーブルから取り出す
        proworktime = i.workproject_time
        nameAndworktime={
            'pname':pname,
            'pworktime':proworktime
            }
        projectwtlist.append(nameAndworktime)

    return projectwtlist

def kintaienterfunc(request):
    return render(request,'kintainyuuryoku.html')