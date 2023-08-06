# cas

这个仓库用于支持 单点登录以及多域名配置

[![Code Health](https://landscape.io/github/unistra/django-cas/master/landscape.svg?style=flat)](https://landscape.io/github/unistra/django-cas/master)
   
CAS client for Django.  This is K-State&#39;s fork of the original, which lives at
https://bitbucket.org/cpcc/django-cas/overview.  This fork is actively maintaned and 
includes several new features.

Current version: 0.8.5

https://github.com/kstateome/django-cas


## Install

    pip install hyperscas

See the document at Bitbucket

https://bitbucket.org/cpcc/django-cas/overview

## Settings.py for CAS

### 把cas 放入INSTALL_APPS下
INSTALLED_APPS += ['cas']

Add the following to middleware if you want to use CAS::
    
    MIDDLEWARE_CLASSES = (
    'cas.middleware.CASMiddleware',
    )
    
### 在urls中增加cas urls的入口
urlpatterns += [
    path("", cas.login, name='home'),
    path("", include("cas.urls")),
]


### 执行makemigrations 命令和migrate命令

### 修改example.json文件，并且移动到项目根目录下的 config/config.json 文件
    最后在python manage.py shell中
    from cas.domain import Domain
    Domain.load()
