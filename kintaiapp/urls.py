from django.conf.urls import url
from . import views
from django.urls import path
from .views import eturanfunc,loginfunc,createfunc,updatemembersfunc,deletemembersfunc
from .viewsdayoff import dayoffallfunc,dayoffcreatefunc, dayoffupdatefunc,dayoffdeletefunc
from .viewsproject import projectallfunc

urlpatterns = [
    #ログイン画面
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
]