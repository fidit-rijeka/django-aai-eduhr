# Django AAI@EduHr

`django-aai-eduhr` is a Django application designed to simplify the integration of your projects with AAI@EduHr, a 
SAML-based Single Sign-On (SSO) service.  It provides a ready-to-use authentication and authorization backend, with 
flexibility for customization and extensions. Additionally, the application includes a management command to quickly 
configure SAML settings, allowing you to focus on development without getting bogged down by configuration tasks.

*This project is not officially affiliated with University Computing Center of University of Zagreb or AAI@EduHr 
project.*

## Overview

Django AAI@EduHr version 1.0.0.

`django-aai-eduhr` is built on top of [djangosaml2](https://djangosaml2.readthedocs.io/) and 
[pysaml2](https://pysaml2.readthedocs.io/en/latest/) and shares much of its configuration with these libraries.

- Supported Python versions: 3.12+
- Supported Django versions: 4.2
- Supported pysaml2 versions: 7.5.x
- Supported djangosaml2 versions: 1.9.x
- Reference LDAP scheme: [hrEdu 1.3.1](https://wiki.srce.hr/download/attachments/65405172/AAI@EduHr-hrEduSheme-2010-v1.3.1.pdf?version=1&modificationDate=1727940424000&api=v2)

The application provides authentication backend with support for authorisation based on configurable
AAI@EduHr attributes. It also supports mapping of AAI data to your custom model fields, including 
related (child) models, and it can normalise multi-valued attributes by creating child model instances for each value.

In addition, the `manage.py aai_quickstart` simplifies the setup of basic SAML configuration, allowing you to 
dive into development right away.
