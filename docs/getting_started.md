# Getting started

## Installation

To get started, create your virtual environment and install the `django-aai-eduhr` package.

```bash
python3 -m venv venv
source venv/bin/activate
pip install django-aai-eduhr
```

## Applications and middleware

Add `djangosaml2` and `django_aai_eduhr` to your `INSTALLED_APPS` setting:

```py
INSTALLED_APPS = [
    # your application

    'django_aai_eduhr',
    'djangosaml2',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]
```

```{hint}
Make sure your application appears before the aforementioned two in the list in case you want to override the default 
403 Forbidden template, which the ACS view renders if the assertions are not valid.
```


Add `djangosaml2.middleware.SamlSessionMiddleware` to your middleware. The middleware ensures `saml_session` attribute 
is set on the request object. Note that it depends on the `django.contrib.sessions.middleware.SessionMiddleware`, so 
the `SamlSessionMiddleware` should appear later in the list.

```py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'djangosaml2.middleware.SamlSessionMiddleware'
]
```

## Authentication backend

Configure the `AAIBackend` authentication backend. You can use it in combinations with other backends or as the only 
authentication backend. 

```py
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_aai_eduhr.backends.AAIBackend',
)
```

It is important to set `SAML_SESSION_COOKIE_SAMESITE` policy to `None`, otherwise browsers won't send the SAML session 
cookie on cross-origin requests, e.g. on successful login. In addition, `SameSite=None` cookies must have `Secure` 
attribute and **will only be sent in secure context**, e.g. HTTPS. See [Web API considerations](web_api.md) for more 
details.

```py
SAML_SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
```

```{hint}
For local development, consider using a reverse proxy with self-signed HTTPS certificates to serve your Django 
application securely. This allows browsers to accept `SameSite=None` cookies, which require a secure (HTTPS) context 
to be sent. Otherwise, you will have to configure `allow_unsolicited: True` in your `SAML_CONFIG`.
```

You can choose whether the backend creates unknown users or rejects authentication.

```py
SAML_CREATE_UNKNOWN_USER = True  # default
```

If you want to authorise only a subset of AAI@EduHr accounts, you can configure the authorisation policy.

```py
AAI_BACKEND_AUTHORISATION = {
    'hrEduPersonPrimaryAffiliation': ['djelatnik'],
    'o': ['uniri'],
    'ou': ['inf']
}
AAI_BACKEND_POLICY = 'all'  # default
```

This will grant access only to the *employees* of *Faculty of Information and Digital Technologies* of *University of 
Rijeka*. Alternatively, you can set the `AAI_BACKEND_POLICY` to `any`. In this case, access will be granted to anyone 
who is an employee, is from University of Rijeka, or is in `inf` organisational unit, regardless of other attributes.

```{note}
This feature only works with `django_aai_eduhr.backends.AAIBackend` and it's derivatives. It is not a feature of the 
base `djangosaml2.backends.Saml2Backend`. You can extend the existing backend or provide your own, see 
[djangosaml2 docs](https://djangosaml2.readthedocs.io/contents/setup.html#custom-user-attributes-processing) for more 
details.
```

## URL configuration

Include `django-aai-eduhr` URLs in your Django project. This will configure AAI@EduHr Login, Logout, ACS and metadata 
views in your project.

```py
from django.urls import path, include

urlpatterns = [
    # other URL patterns
    path('aai/', include('django_aai_eduhr.urls')),
]
```

This adds following URLs to your project:

```
# url         name
aai/login/    # saml2_login
aai/acs/      # saml2_acs
aai/logout/   # saml2_logout
aai/ls/       # saml2_ls
aai/ls/post/  # saml2_ls_post
aai/metadata/ # saml2_metadata
```

You need to configure `LOGIN_URL` where users will be redirected if not logged in, and `ACS_DEFAULT_REDIRECT_URL` where 
users will be redirected to on successful login. You may also configure `LOGOUT_REDIRECT_URL`.

```py
LOGIN_URL = '/aai/login/'  # or reverse_lazy('saml2_login')
ACS_DEFAULT_REDIRECT_URL = LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/thank-you/'
```

```{important}
If your redirect URL is not on the same host as your ACS view, you need to add it to `SAML_ALLOWED_HOSTS`. See 
[djangosaml2 docs](https://djangosaml2.readthedocs.io/contents/setup.html#handling-post-login-redirects) for more 
details.
```

```{note}
Note that the default ACS view first looks up the `next` GET parameter, and only falls back to 
`ACS_DEFAULT_REDIRECT_URL` or `LOGIN_REDIRECT_URL` if the parameter is not present or is invalid.
```

## SAML configuration

The easiest way to configure SAML is to run `manage.py aai_quickstart`. This will start a wizard which 
will guide you through setting up SAML SP endpoint. Upon completion, the wizard will generate copy of your settings 
file including the generated SAML config.

Alternatively, you can override your settings by passing in the `-w` flag, or you can supply a different path by 
passing the `-o <path>` parameter.

```{warning}
The generated settings are not suitable for production. See [production](production.md) for more details.
```

```{important}
If you generated the settings instead of overwriting them, don't forget to point to it by modifying 
`DJANGO_SETTINGS_MODULE` environment variable.
```

If you're looking to configure the endpoint yourself, see 
[djangosaml2](https://djangosaml2.readthedocs.io/contents/setup.html#pysaml2-specific-files-and-configuration) and 
[pysaml](https://pysaml2.readthedocs.io/en/latest/howto/config.html) documentation for more details.

## Attribute mapping

As a next step, you need to configure how AAI@EduHr attributes will map to your `User` and related models. The 
`AAIBackend` can map attributes to your `User` model directly or to the related model holding AAI@EduHr data.

```py

AAI_MODEL = 'app.CustomAAIModel'
AAI_MODEL_RELATED_NAME = 'aai_data'

SAML_DJANGO_USER_MAIN_ATTRIBUTE = 'username'
SAML_DJANGO_USER_MAIN_ATTRIBUTE_LOOKUP = '__iexact'

SAML_ATTRIBUTE_MAPPING = {
    'hrEduPersonUniqueID': ('username',),
    'mail': ('email', ),
    'givenName': ('first_name',),
    'sn': ('last_name',),
    'o': ('aai_data.organisation_name',),
    
    # phone_numbers is a related name of a ForeignKey field defined on the `CustomAAIModel`.
    'mobile': ('aai_data.phone_numbers.number',)  
}
```

`SAML_DJANGO_USER_MAIN_ATTRIBUTE` specifies the identifying (unique) attribute of the `User` model. This is typically 
`username`, but can be other attribute if using custom `User` model.

`SAML_DJANGO_USER_MAIN_ATTRIBUTE_LOOKUP` specifies 
[lookup query](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#field-lookups) for the main attribute.

This configuration will map `NameID` (e.g. `hrEduPersonUniqueId`) to the `username` attribute, and the first 4 
attributes of `SAML_ATTRIBUTE_MAPPING` directly to the `User` model. Organisation name `o` will be mapped to the 
related `app.CustomAAIModel`'s `organisation_name` attribute. Because `mobile` is a multi-valued attribute, it will create
multiple instances of `PhoneNumber` model and associate it to the corresponding `CustomAAIModel`.

In this example, `CustomAAIModel` and `PhoneNumber` would look like the following:

```py
from django.contrib import auth
from django.db import models

class CustomAAIModel(models.Model):
    user = models.OneToOneField(auth.get_user_model(), models.CASCADE, related_name='aai_data')
    organisation_name = models.CharField(max_length=250)

class PhoneNumber(models.Model):
    aai_data = models.ForeignKey('myapp.CustomAAIModel', models.CASCADE, related_name='phone_numbers')
    number = models.CharField(max_length=32)
```

```{important}
Starting from the `User` model, `AAIBackend` traverses relationships up to one level deep for regular attributes, and 
up to two levels deep for multi-valued attributes. **Deeply nested attributes won't be set by the backend.**
```

Target attribute can also be a method defined on the `User` object, in which case it will be called with the attribute 
values. For more details on `SAML_ATTRIBUTE_MAPPING`, consult the 
[djangosaml2 docs](https://djangosaml2.readthedocs.io/contents/setup.html#users-attributes-and-account-linking).


```{warning}
When using AAI@EduHr Lab, i.e. test instance, not all of the configured attributes will be delivered to your 
application. Missing attributes will be logged if `DEBUG=True`, otherwise `ImproperlyConfigured` exception will be 
raised.
```

## Resource registry

Finally, you need to configure the IdP side in the [resource registry](https://registar.aaiedu.hr/) with the matching 
settings. For information on how to register a SAML resource, see the official 
[AAI@EduHr documentation](https://wiki.srce.hr/spaces/AAIUPUTE/pages/66781662/Registar+resursa).

Start by choosing `Univerzalni` *Auth Service*, `basic` *Name Format* and `persistent` *NameId Format*. 
*NameID Attribute* is a unique value identifying each user, and can be one of the following:

- `hrEduPersistentID` - a unique hash value,
- `hrEduUniqueID` - a unique string in the format `<uid>@<realm>`, e.g. `full.name@example.org`, or
- `mail` - an email.

```{note}
Provided authentication backends assume *NameId* format is persistent, but nothing stops you from developing your own
authentication backend which supports transient *NameID* values.
```

In development, you can leave encryption and signing turned off, but it is recommended to turn them on in 
[production](production.md). In any case, your settings should match the settings configured in `SAML_CONFIG`.

Configure URLs pointing to your web application, i.e. entity id, assertion consumer service and single logout service.

Entity ID is a unique identifier that represents your application to AAI@EduHr, typically the URL of your SAML 
metadata. Assertion Consumer Service (ACS) is the endpoint where AAI@EduHr sends authentication responses (SAML 
assertions). Single Logout Service (SLS) is the endpoint used for sending and receiving logout requests and 
responses, enabling user logout across all SAML-connected applications.

If you followed the documentation so far, metadata, assertion consumer service and single 
logout service will be exposed on `/aai/metadata/`, `/aai/acs/`, and `/aai/ls/` paths respectively.

```{hint}
You can use localhost or loopback ip as the domain as long as it's reachable from your clients, which is convenient in 
local development environments.
```

That's it, you can now use AAI@EduHr as an authentication method!