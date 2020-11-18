"""lzkOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include,re_path
import xadmin
from django.views.static import serve
from lzkOnline.settings import MEDIA_ROOT
from django.views.generic import TemplateView
from apps.users.views import ForgetPwdView,ModifyPwdView
from apps.users.views import LoginView,RegisterView,ActiveUserView,ResetView
from apps.organization.views import OrgView,OrgHomeView
from django.views.static import serve
# from lzkOnline.settings import STATIC_ROOT
from apps.users import views


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # path('', TemplateView.as_view(template_name='index.html'),name='index'),

    path("login/",LoginView.as_view(),name="login"),   # login路由
    path("register/",RegisterView.as_view(),name="register"),
    path("captcha/", include("captcha.urls")),  # 验证码
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),
    path("forget/",ForgetPwdView.as_view(),name="forget_pwd"),
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name='reset_pwd'),  # 重置密码激活邮箱的路由
    path("modify_pwd/",ModifyPwdView.as_view(),name="modify_pwd"),               # 修改密码的路由
    # path("org_list/",OrgView.as_view(),name="org_list"),# 这个要删除
    path("org/", include('apps.organization.urls', namespace="org")),
    # 处理图片显示的url，使用django自带serve，传入参数告诉他去那个路径找，
    # 在settings中有配置好了的路径MEDIA_ROOT
    re_path(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),  # 配置文件存储的路径
    path("course/",include("apps.course.urls",namespace="course")),
    # 个人信息
    path("",include("apps.users.urls",namespace="users")),


    # 静态文件    全局配置404和500
    # re_path(r'^static/(?P<path>.*)',serve, {"document_root": STATIC_ROOT }),

    # 文件
    path("media/<path:path>",serve,{"document_root":MEDIA_ROOT}),
    path("ueditor/",include("DjangoUeditor.urls")),

]
# 全局404页面配置
# handler404 = "apps.users.views.page_not_found"
# 全局500页面配置
# handler500 = "apps.users.views.page_error"

