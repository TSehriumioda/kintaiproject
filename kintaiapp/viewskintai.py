from django.http import HttpResponse
from django.shortcuts import render ,redirect
from .models import TMembers,MDayoff,TAttendance,TAttendanceDetail,TWorkDetail,MProject
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout


import datetime
import jpholiday
import calendar

from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

def kintaieturanfunc(request):
    #####年月日を返す
    if request.method == 'POST':
         #確定フラグのたっていない月をリスト化して選択できるようにする
        membersID = request.session['loginmembers_id'] 
        wonth = TAttendance.objects.filter(members_id = membersID,confirm_flg=0)
        wonthlist =[]
        for i in wonth:
            wl = i.year_month
            wonthlist.append(wl)
        print("wonthlist↓")
        print(wonthlist)


        membersID = request.session['loginmembers_id'] 
        workmonth = TAttendance.objects.values_list('year_month').filter(members_id = membersID,confirm_flg=0)

        choosemonth = request.POST['yearmonth']
        print("choooooooooosemonth")
        print(choosemonth) #ここで7月が取れてる！ので後は入れてくのみ

        dt = datetime.date(int(choosemonth[0:4]),int(choosemonth[4:6]),1)
        year = dt.year
        month = dt.month
        print(dt)
        monmon = dt.month
        if monmon < 10:
            MMMM = "0"+str(monmon)
        else:
            MMMM = str(monmon)

        todaysYM = str(year)+MMMM
        wId = TAttendance.objects.get(members_id = membersID,year_month=todaysYM)

        work_Id = wId.work_id

        dtyoubi = calendar.monthrange(year,month)[0]
        dtmonth = calendar.monthrange(year,month)[1]

        w_list = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']
        
        alllist =[]


        kintaidata = TAttendance.objects.get(work_id = work_Id)

        JPholiday = jpholiday.month_holidays(year,month)
        print(len(JPholiday)) #個数をとっているので、祝日のない月は０が帰ってくるのでバグは怒らない

        notholiday = 0
        for i in range(1,dtmonth + 1):
            Date = datetime.datetime(year,month,i)
            if Date.weekday() >= 5 or jpholiday.is_holiday(Date):
                notholiday += 0
            else:
                notholiday += 1
                print(w_list[Date.weekday()])

        answer = notholiday - len(JPholiday)
        roudou = answer * 7.5

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
                times = TAttendanceDetail.objects.get(work_date = days,work=work_Id)

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

                #作業内訳
                workdetailId = TAttendanceDetail.objects.values_list("workdetail_id").get(work_date=days,work=work_Id)
                TWD_list = TWorkDetail.objects.filter(workdetail = workdetailId)
                print("#7")
                projectwtlist = []
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
            'workmonth':wonthlist,
            'month':month,
            'alllist':alllist,
            'zanyuukyuu':kintaidata.yuukyuu_day,
            'late_early':kintaidata.late_early_day,
            'absenceday':kintaidata.absence_day,
            'unpayd_day':kintaidata.unpayd_day,
            'roudou':roudou

        }
        return render(request,'kintaieturan.html',context)

    else:
        #確定フラグのたっていない月をリスト化して選択できるようにする
        membersID = request.session['loginmembers_id'] 
        wonth = TAttendance.objects.filter(members_id = membersID,confirm_flg=0)
        wonthlist =[]
        for i in wonth:
            wl = i.year_month
            wonthlist.append(wl)
        print("wonthlist↓")
        print(wonthlist)
        # workmonth = TAttendance.objects.values_list('year_month').filter(members_id = membersID,confirm_flg=0)


        #TODO：セッションIDからとったメンバ－ズIDで、ユーザのプロジェクトIDをもってくる
        print("メンバID;")
        print(membersID)

        #当月のカレンダーをつくる
        dt = datetime.date.today()
        year = dt.year
        month = dt.month
        print(dt)
        monmon = dt.month
        if monmon < 10:
            MMMM = "0"+str(monmon)
        else:
            MMMM = str(monmon)

        todaysYM = str(year)+MMMM
        wId = TAttendance.objects.get(members_id = membersID,year_month=todaysYM)

        work_Id = wId.work_id

        dtyoubi = calendar.monthrange(year,month)[0]
        dtmonth = calendar.monthrange(year,month)[1]

        w_list = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']
        
        alllist =[]

        #勤怠テーブルの月間所定労働時間、有給休暇日数、遅刻早退、欠勤、その他無給休暇取ってくる

        #有給休暇のこりの日数
        kintaidata = TAttendance.objects.get(work_id = work_Id)
        print("有給")
        print(kintaidata.yuukyuu_day)
        print("遅刻早退")
        print(kintaidata.late_early_day)
        print("欠勤")
        print(kintaidata.absence_day)
        print("その他無給日数")
        print(kintaidata.unpayd_day)

        print("月間所定労働時間")
        JPholiday = jpholiday.month_holidays(year,month)
        print(len(JPholiday)) #個数をとっているので、祝日のない月は０が帰ってくるのでバグは怒らない

        notholiday = 0
        for i in range(1,dtmonth + 1):
            Date = datetime.datetime(year,month,i)
            if Date.weekday() >= 5 or jpholiday.is_holiday(Date):
                notholiday += 0
            else:
                notholiday += 1
                print(w_list[Date.weekday()])

        answer = notholiday - len(JPholiday)
        roudou = answer * 7.5

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
                times = TAttendanceDetail.objects.get(work_date = days,work=work_Id)

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

                #作業内訳
                workdetailId = TAttendanceDetail.objects.values_list("workdetail_id").get(work_date=days,work=work_Id)
                TWD_list = TWorkDetail.objects.filter(workdetail = workdetailId)
                print("#7")
                projectwtlist = []
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
            'workmonth':wonthlist,
            'month':month,
            'alllist':alllist,
            'zanyuukyuu':kintaidata.yuukyuu_day,
            'late_early':kintaidata.late_early_day,
            'absenceday':kintaidata.absence_day,
            'unpayd_day':kintaidata.unpayd_day,
            'roudou':roudou

        }
        return render(request,'kintaieturan.html',context)

def kintaienterfunc(request):
    return render(request,'kintainyuuryoku.html')