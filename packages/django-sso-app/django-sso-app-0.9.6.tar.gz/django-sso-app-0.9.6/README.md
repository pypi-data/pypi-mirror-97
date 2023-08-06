# django-sso-app

User profile management app built upon [django-allauth](https://github.com/pennersr/django-allauth) library
and [cookiecutter-django](https://github.com/pydanny/cookiecutter-django) as scaffold.
Optionally integrates with [kong](https://github.com/Kong/kong) API gateway.

(This is alpha software and is under heavy development)

## Tech

- [python3](https://github.com/python)
- [django](https://github.com/django/django)
- [django-allauth](https://github.com/pennersr/django-allauth)
- [pyjwt](https://github.com/jpadilla/pyjwt)
- [kong](https://github.com/Kong/kong)


## Design decisions

- After login both JWT and Session Token will be sent to the requesting browser
- Single e-mail address for each user
- Django staff users (is_staff and is_superuser) must login through django admin view
- User logout on password change
- New users username is set to email
- While profile completed_at is None user can update username
- When apigateway is enabled, users with completed_at set to None are on "incomplete" group 
- User login on email confirmation 


### Available configurations (Shapes)

1) Backend only:

    Users profile informations are saved into django project with django-sso-app installed.
    
    ```
    DJANGO_SSO_APP_SHAPE = 'backend_only'
    DJANGO_SSO_APP_BACKEND_DOMAINS = ['1.accounts.domain', ...]
    ```

2) Backend + Api Gateway

    As point **1** but with an api gateway (i.e. kong) proxying authenticated requests to backend.
    By logging in the client receives a JWT crafted by backend with the api gateway generated secret.

    ```
    DJANGO_SSO_APP_SHAPE = 'backend_only_apigateway'
    DJANGO_SSO_APP_BACKEND_DOMAINS = ['1.accounts.domain', ...]
    DJANGO_SSO_APP_APIGATEWAY_HOST = 'kong'
    ```

3) Backend + App

    User profile informations are saved into a django-sso-app instance, all protected django projects have
    django-sso-app installed and configured to authenticate users by django-sso-app generated JWT.
    By logging in the client receives a JWT crafted by backend.

    ```
    # Backend config
    DJANGO_SSO_APP_SHAPE = 'backend_app'
    DJANGO_SSO_APP_BACKEND_DOMAINS = ['1.accounts.domain', ..]

    # App config
    DJANGO_SSO_APP_SHAPE = 'app'
    DJANGO_SSO_APP_BACKEND_DOMAINS = ['1.accounts.domain', ...]
    ```

4) Backend + App + Persistence

    As point **3** but protected projects keep user profiles aligned with django-sso-app instance.

    ```
    # Backend config
    DJANGO_SSO_APP_SHAPE = 'backend_app'
    DJANGO_SSO_APP_BACKEND_DOMAINS = ['1.accounts.domain', ...]

    # App config
    DJANGO_SSO_APP_SHAPE = 'app_persistence'
    DJANGO_SSO_APP_BACKEND_DOMAINS = ['1.accounts.domain', ...]
    ```

5) Backend + App + Api Gateway

    As point **3** but with an api gateway proxying authenticated requests to django projects.

    Protected projects authenticate users by the **X-Consumer-Username** header set by api gateway.
    By logging in the client receives a JWT crafted by backend with the api gateway generated secret.
    All requests to protected services are authenticated by the JWT included in cookie (or header).

    ```
    # Backend config
    DJANGO_SSO_APP_SHAPE = 'backend_app_apigateway'
    DJANGO_SSO_APP_BACKEND_DOMAINS = ['1.accounts.domain', ...]
    DJANGO_SSO_APP_APIGATEWAY_HOST = 'http://kong:8001'

    # App config
    DJANGO_SSO_APP_SHAPE = 'app_apigateway'
    DJANGO_SSO_APP_BACKEND_DOMAINS = ['1.accounts.domain', ...]
    ```

6) Backend + App + Persistence + Api Gateway

    As point **5** but protected projects keep user profiles aligned with django-sso-app instance.
    
    ```
    # Backend config
    DJANGO_SSO_APP_SHAPE = 'backend_app_apigateway'
    DJANGO_SSO_APP_BACKEND_DOMAINS = ['1.accounts.domain', ...]
    DJANGO_SSO_APP_APIGATEWAY_HOST = 'http://kong:8001'

    # App config
    DJANGO_SSO_APP_SHAPE = 'app_persistence_apigateway'
    DJANGO_SSO_APP_BACKEND_DOMAINS = ['1.accounts.domain', ...]
    ```


### Note 

Seamless switch between aforementioned configurations is mandatory in order to simplify scaling.


## Setup

### Config vars

#### Required

- APP_DOMAIN
  
  i.e. *accounts.example.com* (default='localhost:8000')

- DJANGO_SSO_APP_SHAPE

   One of *backend_only*, *backend_only_apigateway*, *backend_app*, *app*, *app_persistence*, *app_apigateway*,
   *app_persistence_apigateway* (default='backend_only').


#### Custom (Shape related)

- COOKIE_DOMAIN
  
  JWT cookie domain (default=APP_DOMAIN)


- I18N_PATH_ENABLED
    
  Enables i18n paths (default=True)


- DJANGO_SSO_APP_APIGATEWAY_HOST

  Api gateway instance url (default='http://kong:8001')


- DJANGO_SSO_APP_BACKEND_CUSTOM_FRONTEND_APP
   
  Custom frontend package (default=None)


- DJANGO_SSO_APP_BACKEND_DOMAINS
    
  List of backend domains (default=[APP_DOMAIN])


#### Behaviours

- DJANGO_SSO_APP_LOGOUT_DELETES_ALL_PROFILE_DEVICES 

  Either delete or not other profile devices on logout (default=True)


### Django

#### backend.users.models

```python
from django.contrib.auth.models import AbstractUser
from django_sso_app.core.apps.users.models import DjangoSsoAppUserModelMixin

class User(AbstractUser, DjangoSsoAppUserModelMixin):
    pass
```

#### backend.users.forms

```python
from django_sso_app.backend.users.forms import (UserCreationForm as DjangoSsoAppUserCreationForm,
                                                UserChangeForm as DjangoSsoAppUserChangeForm)

class UserChangeForm(DjangoSsoAppUserChangeForm):
    pass

class UserCreationForm(DjangoSsoAppUserCreationForm):
    pass
```

#### backend.users.admin

```python
from django.contrib import admin
from django.contrib.auth import get_user_model

from django_sso_app.core.apps.users.admin import UserAdmin

User = get_user_model()

admin.site.register(User, UserAdmin)
```

#### settings.py

```python

from django_sso_app.settings import *

DJANGO_SSO_APP_SHAPE = env('DJANGO_SSO_APP_SHAPE', default='backend_only')
DJANGO_SSO_APP_APIGATEWAY_HOST = env('DJANGO_SSO_APP_APIGATEWAY_HOST', default='kong')
BACKEND_CUSTOM_FRONTEND_APP = env('BACKEND_CUSTOM_FRONTEND_APP', default=None)

LOCAL_APPS = ["backend.users.apps.UsersConfig"]  # ...

LOCAL_APPS += DJANGO_SSO_APP_DJANGO_APPS

MIDDLEWARE = [
    ...
    'django_sso_app.core.authentication.backends.DjangoSsoAppLoginAuthenticationBackend',
    
    'django_sso_app.core.authentication.middleware.DjangoSsoAppAuthenticationMiddleware',
    ...
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
] + DJANGO_SSO_APP_DJANGO_AUTHENTICATION_BACKENDS


AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/login/'

DRF_DEFAULT_AUTHENTICATION_CLASSES = [
    'rest_framework.authentication.TokenAuthentication'
    'django_sso_app.core.api.authentication.DjangoSsoApiAuthentication'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': DRF_DEFAULT_AUTHENTICATION_CLASSES,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

```


#### urls.py
```python
urlpatterns = []
api_urlpatterns = []
_I18N_URLPATTERNS = []

from django_sso_app.urls import (urlpatterns as django_sso_app__urlpatterns,
                                 api_urlpatterns as django_sso_app__api_urlpatterns,
                                 i18n_urlpatterns as django_sso_app_i18n_urlpatterns)
from django_sso_app.core.mixins import WebpackBuiltTemplateViewMixin

urlpatterns += django_sso_app__urlpatterns
api_urlpatterns += django_sso_app__api_urlpatterns
_I18N_URLPATTERNS += django_sso_app_i18n_urlpatterns

urlpatterns += [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', ...
]

_I18N_URLPATTERNS += [
    path('', WebpackBuiltTemplateViewMixin.as_view(template_name='pages/home.html'), name='home'),

    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
]

if settings.I18N_PATH_ENABLED:
    urlpatterns += i18n_patterns(
        *_I18N_URLPATTERNS
    )
else:
    urlpatterns += _I18N_URLPATTERNS

```
