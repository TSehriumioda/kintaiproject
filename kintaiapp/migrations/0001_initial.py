# Generated by Django 3.0.8 on 2020-07-26 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MDayoff',
            fields=[
                ('dayoff_id', models.AutoField(db_column='dayoff_Id', primary_key=True, serialize=False)),
                ('dayoff_name', models.CharField(db_column='dayoff_Name', max_length=60)),
                ('dayoff_attribute', models.CharField(db_column='dayoff_Attribute', max_length=10)),
                ('work_time', models.FloatField(db_column='work_Time')),
                ('create_date', models.DateTimeField(db_column='create_Date')),
                ('create_by', models.PositiveIntegerField(db_column='create_By')),
                ('update_date', models.DateTimeField(db_column='update_Date')),
                ('update_by', models.IntegerField(db_column='update_By')),
                ('delete_flg', models.TextField(db_column='delete_Flg')),
            ],
            options={
                'db_table': 'm_dayoff',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MProject',
            fields=[
                ('project_id', models.PositiveIntegerField(db_column='project_Id', primary_key=True, serialize=False)),
                ('project_code', models.PositiveIntegerField(db_column='project_Code')),
                ('project_name', models.CharField(db_column='project_Name', max_length=60)),
                ('project_start', models.DateField(db_column='project_Start')),
                ('project_end', models.DateField(db_column='project_End')),
                ('create_date', models.DateTimeField(blank=True, db_column='create_Date', null=True)),
                ('create_by', models.IntegerField(blank=True, db_column='create_By', null=True)),
                ('update_date', models.DateTimeField(blank=True, db_column='update_Date', null=True)),
                ('update_by', models.IntegerField(blank=True, db_column='update_By', null=True)),
                ('delete_flg', models.IntegerField(db_column='delete_Flg')),
            ],
            options={
                'db_table': 'm_project',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TAttendance',
            fields=[
                ('work_id', models.AutoField(db_column='work_Id', primary_key=True, serialize=False)),
                ('members_id', models.PositiveIntegerField(db_column='members_Id')),
                ('year_month', models.CharField(db_column='year_Month', max_length=6)),
                ('confirm_flg', models.TextField(db_column='confirm_Flg')),
                ('yuukyuu_day', models.PositiveIntegerField(db_column='yuukyuu_Day')),
                ('late_early_day', models.PositiveIntegerField(db_column='late_early_Day')),
                ('unpayd_day', models.PositiveIntegerField(db_column='unpayd_Day')),
                ('absence_day', models.PositiveIntegerField(db_column='absence_Day')),
                ('sammary_work_time', models.FloatField(db_column='sammary_work_Time')),
                ('sammary_actual_work', models.FloatField(db_column='sammary_Actual_Work')),
                ('create_date', models.DateTimeField(db_column='create_Date')),
                ('create_by', models.PositiveIntegerField(db_column='create_By')),
                ('update_date', models.DateTimeField(db_column='update_Date')),
                ('update_by', models.PositiveIntegerField(db_column='update_By')),
            ],
            options={
                'db_table': 't_attendance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TAttendanceDetail',
            fields=[
                ('workdetail_id', models.AutoField(db_column='workdetail_Id', primary_key=True, serialize=False)),
                ('work_date', models.CharField(db_column='work_Date', max_length=2)),
                ('start_time', models.DateTimeField(db_column='start_Time')),
                ('end_time', models.DateTimeField(db_column='end_Time')),
                ('actualwork_time', models.FloatField(db_column='actualwork_Time')),
                ('work_time', models.FloatField(db_column='work_Time')),
                ('break_time', models.FloatField(db_column='break_Time')),
                ('create_date', models.DateTimeField(db_column='create_Date')),
                ('create_by', models.IntegerField(db_column='create_By')),
                ('update_date', models.DateTimeField(db_column='update_Date')),
                ('update_by', models.IntegerField(db_column='update_By')),
            ],
            options={
                'db_table': 't_attendance_detail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TMembers',
            fields=[
                ('members_id', models.PositiveIntegerField(db_column='members_Id', primary_key=True, serialize=False)),
                ('members_name', models.CharField(db_column='members_Name', max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('admin_flg', models.PositiveIntegerField(db_column='admin_Flg')),
                ('allpayd_days', models.PositiveIntegerField(db_column='allpayd_Days')),
                ('create_date', models.DateTimeField(blank=True, db_column='create_Date', null=True)),
                ('create_by', models.CharField(blank=True, db_column='create_By', max_length=20, null=True)),
                ('update_date', models.DateTimeField(blank=True, db_column='update_Date', null=True)),
                ('update_by', models.CharField(blank=True, db_column='update_By', max_length=20, null=True)),
            ],
            options={
                'db_table': 't_members',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TWorkDetail',
            fields=[
                ('workprojectdetail_id', models.AutoField(db_column='workprojectdetail_Id', primary_key=True, serialize=False)),
                ('workproject_time', models.FloatField(db_column='workproject_Time')),
                ('create_date', models.DateTimeField(blank=True, db_column='create_Date', null=True)),
                ('create_by', models.IntegerField(blank=True, db_column='create_By', null=True)),
                ('update_date', models.DateTimeField(blank=True, db_column='update_Date', null=True)),
                ('update_by', models.IntegerField(blank=True, db_column='update_By', null=True)),
            ],
            options={
                'db_table': 't_work_detail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TProjtctMembers',
            fields=[
                ('project', models.OneToOneField(db_column='project_Id', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='kintaiapp.MProject')),
                ('create_date', models.DateTimeField(db_column='create_Date')),
                ('create_by', models.IntegerField(db_column='create_By')),
                ('update_date', models.DateTimeField(db_column='update_Date')),
                ('update_by', models.IntegerField(db_column='update_By')),
            ],
            options={
                'db_table': 't_projtct_members',
                'managed': False,
            },
        ),
    ]