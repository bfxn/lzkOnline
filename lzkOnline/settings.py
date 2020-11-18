import os
import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 让django能识别，自定义apps文件夹
# sys.path.join(0,BASE_DIR)
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8qp)dn$y8&m7srn7@7)4yeh%06&!l!zp^vyp_#supcg1*%_)2j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False
#
# ALLOWED_HOSTS = ['*']


# 重载AUTH_USER_MODEL
AUTH_USER_MODEL = 'users.UserProfile'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'xadmin',
    'crispy_forms',
    'reversion',
    'DjangoUeditor',
    'captcha',
    'pure_pagination',
    'apps.users',
    'apps.course',
    'apps.organization',
    'apps.operation',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lzkOnline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 添加图片处理器，为了在课程列表中前面加上MEDIA_URL
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'lzkOnline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lzk_online',  # 数据库名字
        'USER': 'root',  # 账号
        'PASSWORD': 'lzk123',  # 密码
        'HOST': '127.0.0.1',  # IP
        'PORT': '3306',  # 端口
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# 设置上传文件的路径
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR,"meida")   # 指定一下根目录

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,"static"),
)

AUTHENTICATION_BACKENDS = {
    "apps.users.views.CustomBackend",
}

# EMAIL_HOST = "smtp.qq.com"  # SMTP服务器主机
# EMAIL_PORT = 25             # 端口
# EMAIL_HOST_USER = "2524602321@qq.com"       # 邮箱地址
# EMAIL_HOST_PASSWORD = "dwjybikexxxxxxxx"    # 密码
# EMAIL_USE_TLS= True
# EMAIL_FROM = "2524602321@qq.com"            # 邮箱地址

EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
#发送邮件的邮箱
EMAIL_HOST_USER = 'lzk0103@163.com'
#在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'FOGIEUCOHLAWZPOR'
EMAIL_USE_TLS= True
#收件人看到的发件人
EMAIL_FROM = 'lzk0103@163.com'



# 静态文件
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')



