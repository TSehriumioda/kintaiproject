# from django.conf.urls import url
# from . import views

# urlpatterns = [
#     url('', views.index, name='index'),
# ]
from django.conf.urls import url
from . import views
from django.urls import path
from .views import eturanfunc,loginfunc,createfunc,updatemembersfunc,deletemembersfunc,dayoffallfunc,dayoffcreatefunc

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
    path('dayoff/create/',dayoffcreatefunc,name='dayoffcreate')


]