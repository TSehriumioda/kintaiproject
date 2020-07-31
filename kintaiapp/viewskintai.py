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

        alllist =[]
        
        dayoffid = TAttendanceDetail.objects.values_list("dayoff_id").all
        print(dayoffid)
        w_list = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']
        
        dayoffid = TAttendanceDetail.objects.values_list("dayoff_id").get(work_date=1)
        print(dayoffid)

        #これで外部結合して名前が取得できる
        TAT = TAttendanceDetail.objects.select_related().get(work_date=1)
        dayoffname=TAT.dayoff.dayoff_name
        print(TAT.dayoff.dayoff_name)



        times = TAttendanceDetail.objects.get(work_date=1)
        print(times.start_time.strftime("%H:%M"))
        print(times.end_time.strftime("%H:%M"))
        print(times.break_time)
        print(times.actualwork_time)
        print(times.work_time)

        #作業内訳
        #1日のworkdetail_idをTAttendanceDetailから取得する work_dateは稼働日、work_idは年月
        workdetailId = TAttendanceDetail.objects.values_list("workdetail_id").get(work_date=1,work_id=1)
        #上で取得したworkdetailIdと同じの、TWorkDetailのworkdetailを持ってきて外部結合させてTWDとする
        TWD = TWorkDetail.objects.select_related().filter(workdetail = workdetailId)
        # TWDのworkdetailをもとにプロジェクト名を出す
        projectidlist = []
        projectnamelist =[]
        projectwtlist = []
        print(TWD)

        for i in TWD:
            print(i)
            print(i.project.project_id)
            project_id = i.project.project_id
            print("プロジェクト名")
            pro = MProject.objects.get(project_id=project_id)
            print(pro.project_name)
            pname = pro.project_name
        #   TWDのworkdetailをもとに各作業時間をTWorkdetaiテーブルから取り出す
            print("作業時間")
            print(i.workproject_time)
            proworktime = i.workproject_time
            nameAndworktime={
                'pname':pname,
                'pworktime':proworktime
                }
            print(nameAndworktime)
            projectwtlist.append(nameAndworktime)
        
        print(projectwtlist)

        # print("プロジェクトID")
        # print(TWD.project.project_id)
        # project_id = TWD.project.project_id
        # #プロジェクト名も取り出す
        # print("プロジェクト名")
        # pro = MProject.objects.get(project_id=project_id)
        # print(pro.project_name)
        # #TWDのworkdetailをもとに各作業時間をTWorkdetaiテーブルから取り出す
        # print("作業時間")
        # print(TWD.workproject_time)

        


        for days in range(1,dtmonth + 1):
            # days = 日付作成
            #曜日作成
            today = datetime.datetime(year, month, days)
            a = today.weekday()

            #休暇情報取得 work_dateに入った日数(と他の条件)の休暇情報名前が取れる
            # TAT = TAttendanceDetail.objects.select_related().get(work_date=days)
            # print(TAT.dayoff.dayoff_name)

            #元データ取得
            try:
                T =TAttendanceDetail.objects.get(work_date=days)
                if TAttendanceDetail.objects.get(work_date=days) is "":
                    print("元データなし")
                else:

                    times = TAttendanceDetail.objects.get(work_date=days)
                    
                    
                    #出勤時間取得
                    start_time = times.start_time.strftime("%H:%M")
                    #退勤時間取得
                    end_time = times.end_time.strftime("%H:%M")
                    #休憩時間取得
                    break_time = times.break_time
                    #実働時間取得
                    actual_worktime = times.actualwork_time
                    #労働時間取得
                    work_time = times.work_time

                    #作業内訳
                    

                    #全項目追加
                    # alldata = {'day':days,'youbi':w_list[a]}
                    
                    alldata = {'day':days,'youbi':w_list[a],'dayoffname':dayoffname,'start_time':start_time,
                                'end_time':end_time,'break_time':break_time,'actual_worktime':actual_worktime,'work_time':work_time}

                    alllist.append(alldata)
            except:
                print("つかれたね・・・・・・")
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
                # alldata = {'day':days,'youbi':w_list[a]}
                
                alldata = {'day':days,'youbi':w_list[a],'dayoffname':"",'start_time':start_time,
                            'end_time':end_time,'break_time':break_time,'actual_worktime':actual_worktime,'work_time':work_time}

                alllist.append(alldata)
        



        #当月分の勤怠詳細を持ってくる
        #当月分の勤怠詳細を計算する→結果を出す


        context={
            'workmonth':workmonth,
            'month':month,
            #現在はwork_date=1、work_id=1のもののみ テストデータ入れたらfor文の中に一緒に入れる
            'workdetail':projectwtlist,
            'alllist':alllist,
        }
        return render(request,'kintaieturan.html',context)
###初期画面作成