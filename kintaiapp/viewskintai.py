from django.http import HttpResponse
from django.shortcuts import render ,redirect
from .models import TMembers,MDayoff,TAttendance,TAttendanceDetail,TWorkDetail,MProject,TProjectMembers
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from datetime import datetime 
import datetime
import jpholiday
import calendar
from configparser import ConfigParser

from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

def kintaieturanfunc(request):
    #####年月日を返す
    if request.method == 'POST':
         #確定フラグのたっていない月をリスト化して選択できるようにする
        membersID = request.session['loginmembers_id'] 
        workingmonth = TAttendance.objects.filter(members_id = membersID,confirm_flg=0)
        workingmonthlist =[]
        for i in workingmonth:
            wl = i.year_month
            workingmonthlist.append(wl)
        print("workingmonthlist↓")
        print(workingmonthlist)

        membersID = request.session['loginmembers_id'] 
        workmonth = TAttendance.objects.values_list('year_month').filter(members_id = membersID,confirm_flg=0)

        choosemonth = request.POST['yearmonth']
        print("choooooooooosemonth")
        print(choosemonth) #ここで7月が取れてる！ので後は入れてくのみ

        dt = datetime.date(int(choosemonth[0:4]),int(choosemonth[4:6]),1)
        year = dt.year
        month = dt.month
        print(dt)
        if month < 10:
            MMMM = "0"+str(month)
        else:
            MMMM = str(month)

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
            'workmonth':workingmonthlist,
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
        workingmonth = TAttendance.objects.filter(members_id = membersID,confirm_flg=0)
        workingmonthlist =[]
        for i in workingmonth:
            wl = i.year_month
            workingmonthlist.append(wl)
        print("workingmonthlist↓")
        print(workingmonthlist)
        # workmonth = TAttendance.objects.values_list('year_month').filter(members_id = membersID,confirm_flg=0)

        #TODO：セッションIDからとったメンバ－ズIDで、ユーザのプロジェクトIDをもってくる
        print("メンバID;")
        print(membersID)

        #当月のカレンダーをつくる
        dt = datetime.date.today()
        year = dt.year
        month = dt.month
        print(dt)
        if month < 10:
            MMMM = "0"+str(month)
        else:
            MMMM = str(month)

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
            'workmonth':workingmonthlist,
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
    if request.method == 'POST':
        #送られてきたものを登録する

        membersID = request.session['loginmembers_id'] 
        choosemonth = request.POST['yearmonth']
        context = daysfunc(membersID,choosemonth)

        print("POSTの判定↓")
        print(request.POST['postselect'])
        selectPOST = request.POST['postselect']
        print(selectPOST)

        membersID = request.session['loginmembers_id'] 
        choosemonth = request.POST['yearmonth']
        
        context = daysfunc(membersID,choosemonth)
        return render(request,'kintainyuuryoku.html',context)
    else:
        #日付と曜日のカレンダーをつくる
        membersID = request.session['loginmembers_id'] 
        workingmonth = TAttendance.objects.filter(members_id = membersID,confirm_flg=0)
        workingmonthlist =[]
        for i in workingmonth:
            wl = i.year_month
            workingmonthlist.append(wl)
        print("workingmonthlist↓")
        print(workingmonthlist)

        dt = datetime.date.today()
        year = dt.year
        month = dt.month
        print(dt)

        if month < 10:
            MMMM = "0"+str(month)
        else:
            MMMM = str(month)
        todaysYM = str(year)+MMMM
        wId = TAttendance.objects.get(members_id = membersID,year_month=todaysYM)
        work_Id = wId.work_id

        dtyoubi = calendar.monthrange(year,month)[0]
        dtmonth = calendar.monthrange(year,month)[1]
        w_list = ['月', '火', '水', '木', '金', '土', '日']
        
        #休暇情報のリストを作る
        dayofflist =[]
        dayoffs = MDayoff.objects.all()
        for i in dayoffs:
            dayoffdata={ 'dayoffname':i.dayoff_name,
                         'dayoffid':i.dayoff_id}
            dayofflist.append(dayoffdata)
        print(dayofflist)

        alllist =[]
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
                #データがすでに登録されている場合
                print("#1") 
                times = TAttendanceDetail.objects.get(work_date=days, work=work_Id)
                #出勤時間取得　TODO:時間そのものは取れているので初期値として入るようにする
                start_hour = times.start_time.hour
                start_min = times.start_time.minute
                print(start_hour)
                print(start_min)
                #退勤時間取得
                end_time = times.end_time
                print("#2")
                ####データ全登録                
                alldata = {'day':days,'youbi':w_list[a],'dayoffs':dayoffs,'starthour':start_hour,'startmin':start_min,'endtime':end_time}
                print(alldata)
                print("#3")
                alllist.append(alldata)

            except:
                ####データ全登録 
                print("#5")         
                alldata = {'day':days,'youbi':w_list[a],'dayoffs':dayoffs}
                print("#6")
                print(alldata)
                print("#7")
                alllist.append(alldata)

        #すでに登録されているデータを勤怠テーブル、勤怠詳細テーブルから探してきていれる

        #休暇名を休暇等情報マスタから探してきていれる

        
        context ={
            'alllist':alllist,
            'dayofflist':dayofflist,
            'workmonth':workingmonthlist,
            'chooseYM':todaysYM,
        }

        return render(request,'kintainyuuryoku.html',context)

def kintaichildfunc(request):

    if request.method=='POST':
        #プロジェクトコードで検索をかけた時
        userid = request.session['loginmembers_id']
        print("セッション内のメンバーズID:"+str(userid))
        projectcode= request.POST['projectcode']
        try:
            projects = TProjectMembers.objects.filter(members=userid,project=projectcode)
            print("検索したプロジェクト")
            print(projects)
            projectlist =[]
            for i in projects:
                projectid = i.project.project_id
                projectname= i.project.project_name
                print("projectid:"+str(i)+"番"+str(projectid))
                
                data = {'projectid':projectid,
                        'projectname':projectname,
                        }
                print("data:"+str(data))
                projectlist.append(data)

            A = len(projectlist)
            message= str(A)+"件がヒットしました"

            context={
            'message':message,
            'project':projectlist,
            }
        except:
            context={
                'message':'検索結果が見つかりません',
                'project':projectlist,
            }
        return render(request,'childwindow.html',context)
    else:
        #リンクで飛んできたとき
        userid = request.session['loginmembers_id']
        print("セッション内のメンバーズID:"+str(userid))
        projects = TProjectMembers.objects.filter(members=userid)

        projectlist =[]
        for i in projects:
            projectid = i.project.project_id
            projectname= i.project.project_name
            print("projectid:"+str(i)+"番"+str(projectid))
            
            data = {'projectid':projectid,
                    'projectname':projectname
                    }
            print(data)
            projectlist.append(data)

        print(projectlist)
        context={
            'project':projectlist,
        }

        return render(request,'childwindow.html',context)

def daysfunc(membersID,choosemonth):
    print("## daysfuncresult ##")
    workingmonth = TAttendance.objects.filter(members_id = membersID,confirm_flg=0)
    workingmonthlist =[]
    for i in workingmonth:
        wl = i.year_month
        workingmonthlist.append(wl)

    workmonth = TAttendance.objects.values_list('year_month').filter(members_id = membersID,confirm_flg=0)
    dt = datetime.date(int(choosemonth[0:4]),int(choosemonth[4:6]),1)
    year = dt.year
    month = dt.month
    
    if month < 10:
        MMMM = "0"+str(month)
    else:
        MMMM = str(month)
    todaysYM = str(year)+MMMM
    wId = TAttendance.objects.get(members_id = membersID,year_month=todaysYM)
    work_Id = wId.work_id

    dtyoubi = calendar.monthrange(year,month)[0]
    dtmonth = calendar.monthrange(year,month)[1]
    w_list = ['月', '火', '水', '木', '金', '土', '日']
    
    #休暇情報のリストを作る
    dayofflist =[]
    dayoffs = MDayoff.objects.all()
    for i in dayoffs:
        dayoffdata={ 'dayoffname':i.dayoff_name,
                        'dayoffid':i.dayoff_id}
        dayofflist.append(dayoffdata)

    alllist =[]
    for days in range(1,dtmonth + 1):
        # days = 日付作成
        #曜日作成

        today = datetime.datetime(year, month, days)
        a = today.weekday()

        try:
            #データがすでに登録されている場合
            print("#1") #TODO:ここでデータ取れなくなっているのでここから再開
            times = TAttendanceDetail.objects.get(work_date=days, work=work_Id)
            #出勤時間取得　時間そのものは取れているので後日直す
            start_hour = times.start_time.hour
            start_min = times.start_time.minute
            #退勤時間取得
            end_time = times.end_time
            print("#2")
            ####データ全登録                
            alldata = {'day':days,'youbi':w_list[a],'dayoffs':dayoffs,'starthour':start_hour,'startmin':start_min,'endtime':end_time}
            print("#3")
            alllist.append(alldata)

        except:
            ####データ全登録 
            print("#5")         
            alldata = {'day':days,'youbi':w_list[a],'dayoffs':dayoffs}
            print("#6")
            print("#7")
            alllist.append(alldata)

    #すでに登録されているデータを勤怠テーブル、勤怠詳細テーブルから探してきていれる

    #休暇名を休暇等情報マスタから探してきていれる

    
    context ={
        'alllist':alllist,
        'dayofflist':dayofflist,
        'workmonth':workingmonthlist,
        'chooseYM':todaysYM,     
    }

    return context

def kintaitouroku(request):
    if request.method == 'POST':
        membersID = request.session['loginmembers_id'] 
        yearmonth = request.POST['yearmonth']
        print(yearmonth)
        now = datetime.datetime.now()
        dt = datetime.date(int(yearmonth[0:4]),int(yearmonth[4:6]),1)
        year = dt.year
        month = dt.month
        dtmonth = calendar.monthrange(year,month)[1]
        ##work_idをTAttendanceからもってくる
        work_id = TAttendance.objects.get(members_id=membersID,year_month=yearmonth)
        print("work_id:"+str(work_id))
        tourokulist = []
        for day in range(1,dtmonth+1):
            dayoffs = request.POST['dayoff'+str(day)]
            starttime = request.POST['starttime'+str(day)]
            endtime = request.POST['endtime'+str(day)]
            
            if day < 10:
                day = "0"+str(day)

            if starttime != "" and endtime != "":
                s_time = yearmonth+str(day)+starttime
                e_time = yearmonth+str(day)+endtime
                start_time = datetime.datetime.strptime(s_time, '%Y%m%d%H:%M')
                end_time = datetime.datetime.strptime(e_time, '%Y%m%d%H:%M')
                print("endtime:"+str(end_time))
                print("start_time:"+str(start_time))
                print("dayoffs:"+str(dayoffs))
                ##TODO: 実働時間、休憩時間の計算と作成者、作成日時、更新者、更新日時の登録
                ##worktime
                WT = end_time - start_time
                print(WT)
                print(type(WT))
                hourminutes = str(WT)
                hour = hourminutes.split(":")
                print("hour"+str(hour[0]))
                print("minutes:"+str(hour[1]))
                culhour = int(hour[1])
                if   culhour >= 0 and culhour <= 15:
                    minutes = 0.15
                elif culhour >= 16 and culhour <= 30:
                    minutes = 0.30
                elif culhour  >= 31 and culhour <= 45:
                    minutes = 0.75
                else:
                    minutes = 1
                
                work_time = float(hour[0]) + float(minutes)
                print("work_time:"+str(work_time))

                ##breaktime
                config = ConfigParser()
                config_url = r'C:\Users\steru\Desktop\kinntai\kintai\kintaiproject\kintaiapp\config.ini' 
                config.read(config_url)

                actualwork_time = 0
                breaktime = 0
                if work_time < 5:
                    breaktime = config.get('breaktime0','bt0')
                    actualwork_time = work_time - float(breaktime)
                elif work_time >= 5 and work_time < 8.5:
                    breaktime = config.get('breaktime1','bt1')
                    actualwork_time = work_time - float(breaktime)
                elif work_time >= 8.5:
                    breaktime = config.get('breaktime2','bt2')
                    actualwork_time = work_time - float(breaktime)

                print("breaktime:"+str(breaktime))
                print("actualworktime(cul):"+str(actualwork_time))
                ## worktime
                break_time = float(breaktime)

                print("＃登録")
                day_offid = int(day)
                ##TODO:dateが０１の状態になってしまうのでなんかうまいこと修正する　listで文字列を1文字ずつ切り分けられる
                print("list[1]のday:"+str(day))
                date = str(day)
                splitdate = list(date)
                if splitdate[0] == "0":
                    date = splitdate[1]
                print("返還後のdate:"+str(date))



                TOUROKU= TAttendanceDetail(work=work_id,work_date=date,
                                           start_time=start_time,end_time=end_time,break_time=break_time,work_time=work_time,
                                           actualwork_time= actualwork_time,create_date=now, update_date=now,
                                           create_by=membersID,update_by=membersID)
                print(TOUROKU)
                TOUROKU.save()
                           
                
        context = daysfunc(membersID,yearmonth)
        return render(request,'kintainyuuryoku.html',context)
    else:
        membersID = request.session['loginmembers_id'] 
        choosemonth = datetime.date.today().strftime('%Y%m')
        print(choosemonth)
        context = daysfunc(membersID,choosemonth)
        return render(request,'kintainyuuryoku.html',context)