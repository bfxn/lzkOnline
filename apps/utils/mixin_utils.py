# 当用户点击 开始学习 后，应该把这门课程与用户关联起来
# 但是在这之前要进行一个判断，如果没有登录，应该先让用户登录才行
# 如果是用函数方式写，直接加个装饰器（@login_required）就行，但是，我们是用类方式写的，必须用继承


##  最基本的类都放在这儿    ##
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url="/login/"))
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMixin,self).dispatch(request,*args,**kwargs)



