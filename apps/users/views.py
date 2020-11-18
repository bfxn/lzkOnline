from django.core.paginator import PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django_redis.serializers import json

from apps.course.models import Course
from apps.operation.models import UserCourse, UserFavorite, UserMessage
from apps.organization.models import CourseOrg, Teacher
from apps.utils.mixin_utils import LoginRequiredMixin
from .models import UserProfile, Banner
from django.db.models import Q
from django.views.generic.base import View
from apps.users.forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from django.contrib.auth.hashers import make_password
from apps.utils.email_send import send_register_email
from apps.users.models import EmailVerifyRecord


""" 首页 """
class IndexView(View):
    def get(self,request):
        # 轮播图
        all_banners = Banner.objects.all().order_by("index")
        # 课程
        courses = Course.objects.filter(is_banner=False)[:6]
        # 轮播课程
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        # 课程机构
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request,"index_bak.html",{
            "all_banners":all_banners,
            "courses":courses,
            "banner_courses":banner_courses,
            "course_orgs":course_orgs,

        })



# 邮箱和用户名都可以登录
# 基础ModelBackend类，因为他有authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因，Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))

            # django后的后台中密码加密：所以不能password=password
            # UserProfile继承的AbstractUser中有def check_password(self,raw_pasword)
            if user.check_password(password):
                return user

        except Exception as e:
            return None


# 首页—首先判断当前用户是否登录，登录就展示用户名和个人信息，否则就显示登录注册
# 增加邮箱登录—让用户可以通过邮箱或者用户名都可以登录，自定了authenticate方法↑↑↑
        # 在user表中还需要添加两个功能独立的表：EmailVerifyRecord邮箱和Banner轮播图
# 然后完善一下登录页面的错误信息显示
# 登录视图
class LoginView(View):
    def get(self,request):
        return render(request,"login.html")

    def post(self,request):
        # 实例化
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取用户提交的用户名和密码
            user_name = request.POST.get("username",None)
            pass_word = request.POST.get("password",None)
            # 成功返回user对象，失败None
            user = authenticate(username=user_name,password=pass_word)
            # 如果不是null说明验证成功
            if user is not None:
                if user.is_active == 1:
                    # 只有注册激活才能登录
                    # 登录
                    login(request,user)
                elif user.is_active == 0:
                    return render(request,"login.html",{"msg":"用户未激活，请激活后再登陆！"})
                # return render(request,'index.html')
                return HttpResponseRedirect(reverse("index"))
            # 只有当用户名和密码不存在时，才返回错误信息到前端
            else:
                return render(request,"login.html",{"msg":"用户名或密码错误","login_form":login_form})

        # form.is_valid()已经判断不合法了，所以这里不需要再返回错误信息到前端了
        else:
            return render(request,"login.html",{"login_form":login_form})




# 在python中内置有一个smtp邮件发送模块，在django中有封装
# 直接在settings中设置就行

# 激活用户
class ActiveUserView(View):
    def get(self,request,active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功跳转到登录页面
                return redirect(reverse("login"))
        # 自己瞎输的验证码
        else:
            return render(request, "register.html", {"msg": "您的激活链接无效"})



# 用户输入邮箱，密码和验证码，然后点击注册，如果输入不正确，提示错误信息
# 如果表单验证通过，然后发送给客户激活邮件，用户通过邮件链接激活以后才能登录
# # 即使注册成功，没有激活的用户也不能登录

# forms中定义验证码registerForm，（字段：captcha-）
# post请求的时候实例化form表单验证
# register.html中添加{{register_form.captcha}}
# 然后在注册页面中就生成了验证码，提交表单验证，成功就跳转到登录，验证失败就提示error_messages错误信息
# 注册视图
class RegisterView(View):
    '''用户注册'''
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # print(1111)
            user_name = request.POST.get('email', None)
            # print(user_name)
            # 如果用户已存在，则提示错误信息
            if UserProfile.objects.filter(email = user_name):
                return render(request, 'register.html', {'register_form':register_form,'msg': '用户已存在'})

            pass_word = request.POST.get('password', None)
            # 实例化一个user_profile对象
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 对保存到数据库的密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name,"register")
            return render(request,'login.html')
        else:
            # print(888)
            return render(request,'register.html',{'register_form':register_form})




# 如果用户忘记密码，在登录页面有点击密码按钮，跳转到找回密码页面
# 在页面http://127.0.0.1:8000/forget/，输入用户邮箱和验证码，然后发送找回密码邮件提醒
# 然后通过邮件中的链接，跳转到http://127.0.0.1:8000/reset/xxxxxxx，然后重置密码

# 找回密码
class ForgetPwdView(View):
    """ 找回密码 """
    def get(self,request):   # get方式直接返回忘记密码的表单
        forget_form = ForgetPwdForm()
        return render(request,"forgetpwd.html",{"forget_form":forget_form})

    def post(self,request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email",None)
            send_register_email(email,"forget")
            return render(request,"send_success.html")
        else:
            return render(request,"forgetpwd.html",{'forget_form':forget_form})

# 重置密码
class ResetView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,"password_reset.html",{"email":email})
        else:
            return render(request,"active_fail.html")
        return render(request,"login.html")

# 修改密码的视图
class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            email = request.POST.get("email","")
            if pwd1 != pwd2:
                return render(request,"password_reset.html",{"email":email,"msg":"您的两次密码输入不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request,"login.html")
        else:
            email = request.POST.get("email","")
            return render(request,"password_reset.html",{"email":email,"modify_form":modify_form})


from django.urls import reverse
# 用户退出

class LogoutView(View):
    """ 用户退出 """
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))



# 用户个人信息
class UserinfoView(LoginRequiredMixin,View):
    """ 用户个人信息 """
    def get(self,request):
        return render(request,"./users/usercenter-info.html",{})
    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


# 用户图像修改
class UploadImageView(LoginRequiredMixin,View):
    """ 用户图像修改 """
    def post(self,request):
        # 上传的文件都在request.FILES里面获取，所以这里要多传一个这个参数
        image_form = UploadImageForm(request.POST,request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')



# 个人中心修改用户密码
class UpdatePwdView(View):
    """ 个人中心修改用户密码 """
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致，重新输入"}',  content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')




# 用户中心发送邮箱修改验证码
class SendEmailCodeView(LoginRequiredMixin,View):
    """ 发送邮箱修改验证码 """
    def get(self,request):
        email = request.GET.get("email","")

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在，请重新输入"}', content_type='application/json')

        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')



# 修改邮箱
class UpdateEmailView(LoginRequiredMixin, View):
    '''修改邮箱'''
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')



class MyCourseView(LoginRequiredMixin,View):
    """ 我的课程 """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "users/usercenter-mycourse.html", {
            "user_courses":user_courses,

        })


# 我的收藏--课程机构
class MyFavOrgView(LoginRequiredMixin,View):
    """ 我收藏的课程机构 """
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        # 上面的fav_orgs只是存放了id。我们还需要通过id找到机构对象
        # 然后对他进行遍历
        for fav_org in fav_orgs:
            # 取出fav_id也就是机构的id。
            org_id = fav_org.fav_id
            # 获取这个机构对象
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, "users/usercenter-fav-org.html", {
            "org_list": org_list,

        })


# 我收藏的授课讲师
class MyFavTeacherView(LoginRequiredMixin,View):
    """ 我收藏的授课讲师 """

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, "users/usercenter-fav-teacher.html", {
            "teacher_list": teacher_list,

        })


# 我的收藏--公开课程
class MyFavCourseView(LoginRequiredMixin,View):
    """ 我收藏的课程 """
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'users/usercenter-fav-course.html', {
            "course_list":course_list,

        })


# 我的消息
class MyMessageView(LoginRequiredMixin,View):
    """ 我的消息 """
    def get(self,request):
        all_message = UserMessage.objects.filter(user=request.user.id)

        try:
            page = request.GET.get("page",1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 4)
        messages = p.page(page)
        return  render(request, "users/usercenter-message.html", {
            "messages":messages,

        })




from django.shortcuts import render_to_response
def pag_not_found(request):
    # 全局404处理函数
    response = render_to_response('../templates/errors/404.html', {})
    response.status_code = 404
    return response

def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('../templates/errors/500.html', {})
    response.status_code = 500
    return response



