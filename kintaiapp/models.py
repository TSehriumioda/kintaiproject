from django.db import models
from django.utils import timezone

class MDayoff(models.Model):
    dayoff_id = models.AutoField(db_column='dayoff_Id', primary_key=True)  # Field name made lowercase.
    dayoff_name = models.CharField(db_column='dayoff_Name', max_length=60)  # Field name made lowercase.
    dayoff_attribute = models.CharField(db_column='dayoff_Attribute', max_length=10)  # Field name made lowercase.
    work_time = models.FloatField(db_column='work_Time')  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='create_Date')  # Field name made lowercase.
    create_by = models.PositiveIntegerField(db_column='create_By')  # Field name made lowercase.
    update_date = models.DateTimeField(db_column='update_Date')  # Field name made lowercase.
    update_by = models.IntegerField(db_column='update_By')  # Field name made lowercase.
    delete_flg = models.PositiveIntegerField(db_column='delete_Flg')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'm_dayoff'


class MProject(models.Model):
    project_id = models.PositiveIntegerField(db_column='project_Id', primary_key=True)  # Field name made lowercase.
    project_code = models.PositiveIntegerField(db_column='project_Code')  # Field name made lowercase.
    project_name = models.CharField(db_column='project_Name', max_length=60)  # Field name made lowercase.
    project_start = models.DateField(db_column='project_Start')  # Field name made lowercase.
    project_end = models.DateField(db_column='project_End')  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='create_Date', blank=True, null=True)  # Field name made lowercase.
    create_by = models.IntegerField(db_column='create_By', blank=True, null=True)  # Field name made lowercase.
    update_date = models.DateTimeField(db_column='update_Date', blank=True, null=True)  # Field name made lowercase.
    update_by = models.IntegerField(db_column='update_By', blank=True, null=True)  # Field name made lowercase.
    delete_flg = models.IntegerField(db_column='delete_Flg')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'm_project'


class TAttendance(models.Model):
    work_id = models.AutoField(db_column='work_Id', primary_key=True)  # Field name made lowercase.
    members_id = models.PositiveIntegerField(db_column='members_Id')  # Field name made lowercase.
    year_month = models.CharField(db_column='year_Month', max_length=6)  # Field name made lowercase.
    confirm_flg = models.TextField(db_column='confirm_Flg')  # Field name made lowercase. This field type is a guess.
    yuukyuu_day = models.PositiveIntegerField(db_column='yuukyuu_Day')  # Field name made lowercase.
    late_early_day = models.PositiveIntegerField(db_column='late_early_Day')  # Field name made lowercase.
    unpayd_day = models.PositiveIntegerField(db_column='unpayd_Day')  # Field name made lowercase.
    absence_day = models.PositiveIntegerField(db_column='absence_Day')  # Field name made lowercase.
    sammary_work_time = models.FloatField(db_column='sammary_work_Time')  # Field name made lowercase.
    sammary_actual_work = models.FloatField(db_column='sammary_Actual_Work')  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='create_Date')  # Field name made lowercase.
    create_by = models.PositiveIntegerField(db_column='create_By')  # Field name made lowercase.
    update_date = models.DateTimeField(db_column='update_Date')  # Field name made lowercase.
    update_by = models.PositiveIntegerField(db_column='update_By')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_attendance'

class TAttendanceDetail(models.Model):
    workdetail_id = models.AutoField(db_column='workdetail_Id', primary_key=True)  # Field name made lowercase.
    work = models.ForeignKey(TAttendance, models.DO_NOTHING, db_column='work_Id')  # Field name made lowercase.
    work_date = models.CharField(db_column='work_Date', max_length=4)  # Field name made lowercase.
    dayoff = models.ForeignKey(MDayoff, models.DO_NOTHING, db_column='dayoff_Id')  # Field name made lowercase.
    start_time = models.DateTimeField(db_column='start_Time')  # Field name made lowercase.
    end_time = models.DateTimeField(db_column='end_Time')  # Field name made lowercase.
    actualwork_time = models.FloatField(db_column='actualwork_Time')  # Field name made lowercase.
    work_time = models.FloatField(db_column='work_Time')  # Field name made lowercase.
    break_time = models.FloatField(db_column='break_Time')  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='create_Date')  # Field name made lowercase.
    create_by = models.IntegerField(db_column='create_By')  # Field name made lowercase.
    update_date = models.DateTimeField(db_column='update_Date')  # Field name made lowercase.
    update_by = models.IntegerField(db_column='update_By')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_attendance_detail'



class TMembers(models.Model):
    members_id = models.PositiveIntegerField(db_column='members_Id', primary_key=True)  # Field name made lowercase.
    members_name = models.CharField(db_column='members_Name', max_length=20)  # Field name made lowercase.
    password = models.CharField(max_length=20)
    admin_flg = models.IntegerField(db_column='admin_Flg')  # Field name made lowercase.
    allpayd_days = models.PositiveIntegerField(db_column='allpayd_Days')  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='create_Date', blank=True, null=True)  # Field name made lowercase.
    create_by = models.CharField(db_column='create_By', max_length=20, blank=True, null=True)  # Field name made lowercase.
    update_date = models.DateTimeField(db_column='update_Date', blank=True, null=True)  # Field name made lowercase.
    update_by = models.CharField(db_column='update_By', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_members'

class TProjectMembers(models.Model):
    project = models.OneToOneField(MProject, models.DO_NOTHING, db_column='project_Id', primary_key=True)  # Field name made lowercase.
    members = models.ForeignKey(TMembers, models.DO_NOTHING, db_column='members_Id')  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='create_Date')  # Field name made lowercase.
    create_by = models.IntegerField(db_column='create_By')  # Field name made lowercase.
    update_date = models.DateTimeField(db_column='update_Date')  # Field name made lowercase.
    update_by = models.IntegerField(db_column='update_By')  # Field name made lowercase.
    delete_flg = models.PositiveIntegerField(db_column='delete_Flg', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_project_members'
        unique_together = (('project', 'members'),)




class TWorkDetail(models.Model):
    workprojectdetail_id = models.AutoField(db_column='workprojectdetail_Id', primary_key=True)  # Field name made lowercase.
    workdetail = models.ForeignKey(TAttendanceDetail, models.DO_NOTHING, db_column='workdetail_Id')  # Field name made lowercase.
    project = models.ForeignKey(MProject, models.DO_NOTHING, db_column='project_Id')  # Field name made lowercase.
    workproject_time = models.FloatField(db_column='workproject_Time')  # Field name made lowercase.
    create_date = models.DateTimeField(db_column='create_Date', blank=True, null=True)  # Field name made lowercase.
    create_by = models.IntegerField(db_column='create_By', blank=True, null=True)  # Field name made lowercase.
    update_date = models.DateTimeField(db_column='update_Date', blank=True, null=True)  # Field name made lowercase.
    update_by = models.IntegerField(db_column='update_By', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_work_detail'