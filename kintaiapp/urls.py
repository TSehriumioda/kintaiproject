from django.conf.urls import url
from django.urls import path
from .viewsaccount import loginfunc,logoutfunc
from .viewsmembers import eturanfunc,createfunc,updatemembersfunc,deletemembersfunc
from .viewsdayoff import dayoffallfunc,dayoffcreatefunc, dayoffupdatefunc,dayoffdeletefunc
from .viewsproject import projectallfunc,projectcreatefunc,projectdeletefunc,projectupdatefunc
from .viewskintai import kintaieturanfunc,kintaienterfunc,kintaichildfunc ,kintaitouroku


urlpatterns = [
    #ログイン画面
    path('logout/',logoutfunc,name='logout'),
    path('login/',loginfunc,name='login'),
    #社員管理画面
    path('members/all/',eturanfunc,name='eturan'),
    path('members/create/',createfunc,name='create'),
    path('members/update/',updatemembersfunc,name='updatemembers'),
    path('members/delete/',deletemembersfunc,name='deletemembers'),
    #休暇等情報管理画面
    path('dayoff/all/',dayoffallfunc,name='dayoffall'),
    path('dayoff/create/',dayoffcreatefunc,name='dayoffcreate'),
    path('dayoff/update/', dayoffupdatefunc,name='dayoffupdate'),
    path('dayoff/delete/',dayoffdeletefunc,name='dayoffdelete'),
    #プロジェクト管理画面
    path('project/all/',projectallfunc,name='projectall'),
    path('project/create/',projectcreatefunc,name='projectcreate'),
    path('project/update/',projectupdatefunc,name='projectupdate'),
    path('project/delete/',projectdeletefunc,name='projectdelete'),
    #共通画面
    path('common/eturan/',kintaieturanfunc,name='kintaieturan'),
    path('common/enter/',kintaienterfunc,name='kintaienter'),
    path('common/child/',kintaichildfunc,name='kintaichild'),
    path('common/touroku/',kintaitouroku,name='kintaitouroku'),
]