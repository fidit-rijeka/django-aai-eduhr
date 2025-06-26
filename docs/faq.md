# Frequently asked questions

## 1. Why do I have to set up HTTPS for my local development environment?

`djangosaml2` and by extension `django_aai_eduhr` tracks AAI@EduHr session using `saml_session` cookie. When a user 
successfully logs in, the application associates SSO session with the cookie. During this process,
AAI@EduHr will trigger a POST request from the client to the application with the `Origin` header set to AAI@EduHr 
domain. 

If `saml_session` cookie does not have `SameSite=None`, **it will not be sent to the application because 
the aforementioned POST request is a cross-origin request**. This means that the application won't be able to 
determine if the user has signed in or not.

In 2020, all major browsers imposed a restriction where `SameSite=None` cookies will only be sent in secure 
context, i.e. decorated with `Secure` attribute and transmitted over HTTPS.

## 2. Why do I get "Authentication Error" page on successful login?

Your client is most likely not sending `saml_session` cookie, please verify if this is the case.

## 3. How can I display something other than "Authentication Error" page when a sign-on request fails?

You can change the display by overriding `djangosaml2/login_error.html` template rendered by 
`djangosaml.views.AssertionConsumerServiceView`. You can also subclass the view itself if you need to customize 
rendering logic, e.g. to add custom context data.

## 4. How can I run custom code before or after user has logged in?

`django_aai_eduhr.backends.AAIBackend` sends `django_aai_eduhr.signals.aai_pre_update` and 
`django_aai_eduhr.signals.aai_post_update` signals before and after it processes AAI@EduHr data. You can register 
listeners for these signals as you would for any other Django signal.

```py
from django.dispatch import receiver
import logging

import django_aai_eduhr.signals

logger = logging.getLogger(__name__)

@receiver(django_aai_eduhr.signals.aai_pre_update)
def on_pre_update(sender, **kwargs):
    user = kwargs['user']
    logger.info(f'Started processing AAI data for user: {user.get_full_name()}')

@receiver(django_aai_eduhr.signals.aai_post_update)
def on_post_update(sender, **kwargs):
    user = kwargs['user']
    logger.info(f'Finished processing AAI data for user: {user.get_full_name()}')
```

Alternatively, you can subclass [the backend](api/django_aai_eduhr.backends.rst).
