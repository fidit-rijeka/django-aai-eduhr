# Production

Deploying an application which makes use of `django-aai-eduhr` to production takes a bit more effort, nevertheless it 
is only a matter of configuration. The `manage.py aai_quickstart` command generates SAML configuration suitable for 
development, but these settings are not necessarily secure, and incur minor performance penalty.

```{hint}
This is not an exhaustive list of security related settings by any means, see 
[pysaml2 docs](https://pysaml2.readthedocs.io/en/latest/howto/config.html#configuration-directives) for more options 
like used algorithms, certificate validation, etc.
```

## Security

Depending on your security requirements, and the data you exchange with AAI@EduHr IdP, you need to enable signing and 
encryption. If you don't exchange personal information, you may get away with signing only. This ensures that IdP and 
SP can detect if messages have been tampered with during transmission, for example in case of man-in-the-middle 
attacks. If you do exchange personal information, for example `hrEduPersonOIB`, it is strongly advised to enable 
encryption as well. In any case, these come with a bit of a performance overhead, so they're disabled by default in the
development configuration.

### Signing

Depending on your configuration, you should enable *Sign Assertion*, *Sign Response* and *Sign Logout* in the 
AAI@EduHr resource registry. You should configure your certificate/public key in the *SP Signing Certificate* field 
without the `-----BEGIN/END CERTIFICATE-----` lines. This will enable signing and validation of exchanged messages by 
the IdP.

On the application side, you should enable `want_assertions_signed` and `want_responses_signed`. If you want your 
application to sign logout and/or authentication requests, you should enable `authn_requests_signed` and/or 
`logout_requests_signed` as well.

```py
SAML_CONFIG = {
    # extra configuration removed for clarity
    
    'service': {
        'sp': {
            'want_assertions_signed': True,  # validate signed assertions
            'want_response_signed': True,  # validate signed responses
            
            'authn_requests_signed': True,  # sign authentication requests
            'logout_requests_signed': True,  # sign logout requests
        },
    },
}
```

If you enabled signing on the SP side, you should enable *Validate Authn Request*, *Validate Logout Request* and 
*Validate Redirect* respectively.

Finally, configure the path to your certificate and corresponding private key which the SP will use for signing and 
validation.

```py
SAML_CONFIG = {
    # extra configuration removed for clarity
    
    'key_file': '/path/to/my/signing_key.pem',
    'cert_file': '/path/to/my/signing_certificate.pem'
}
```

### Encryption

For the encryption, you should enable *Encrypt Assertion* and/or *NameID Encryption*, and then configure the 
encryption certificate. On the SP side you should configure both the certificate and the corresponding 
private key.

```py
SAML_CONFIG = {
    # extra configuration removed for clarity
    
    'encryption_keypairs': [
        {
            'key_file': '/path/to/my/encryption_key.pem',
            'cert_file': '/path/to/my/encryption_certificate.pem'
        }
    ],
}
```

### Bearer Assertion Replay

The backend provided by the `django_aai_eduhr.backends` includes built-in protection against bearer assertion replay 
attacks. However, this protection requires proper configuration to function correctly.

If you're developing a custom authentication backend and do not inherit from `django_aai_eduhr.backends.AAIBackend`, 
you can still enable replay attack mitigation by including `django_aai_eduhr.backends.AssertionReplayMitigationMixin`. 
This mixin implements the necessary logic to prevent the reuse of previously processed assertions.

The mixin relies on Django's caching framework to temporarily store identifiers from processed assertions. It also 
checks the `NotOnOrAfter` attribute of each assertion to ensure it hasn't expired. Once an assertion is used, 
it is recorded in the cache and will be rejected if seen again.

Because the mitigation logic depends on the cache, it is essential that your Django project has a correctly configured 
caching backend. In production environments, where your application may run in multiple processes (e.g., multiple 
Gunicorn workers), your cache must support cross-process caching.

By default, if you haven't explicitly configured caching, Django uses the 
[local memory cache](https://docs.djangoproject.com/en/4.2/topics/cache/#local-memory-caching), which **is not** 
shared between processes. This can result in replay attack protection silently failing, as each process maintains its 
own isolated cache.

To ensure proper functionality, you must use a cache backend that supports shared access across processes, such as 
Redis or Memcached, but any cache that implements the Django cache API is compatible.

You can choose which cache `django_aai_eduhr.backends.AssertionReplayMitigationMixin` will use by changing 
`AAI_ASSERTION_CACHE` setting which is `default` if not explicitly configured.

## Metadata

Exchange of metadata facilitates the automatic configuration of SAML entities by sharing important information about 
each party's endpoints, capabilities, and configurations. This can be achieved by preloading the metadata locally, 
automatic retrieval from the remote URL or through an 
[MDQ service](https://pysaml2.readthedocs.io/en/latest/howto/config.html#configuration-directives).

The `manage.py aai_quickstart` command sets up remote retrieval of IdP's metadata, but this slows down performance 
since network IO is slower than local disk IO. You can configure your application to load metadata locally which will 
improve performance.

```py
SAML_CONFIG = {
    # extra configuration removed for clarity
    
    'metadata': {
        'local': ['/path/to/idp/metadata.xml']
    },
}
```

You can obtain the production and the AAI@EduHr Lab metadata by downloading it from the link provided in the 
[AAI@EduHr documentation](https://wiki.srce.hr/spaces/AAIUPUTE/pages/69501694/SAML+metapodaci+SSO+servisa), under the 
"All SAML implementations" section.

## Description

You can provide human-readable information about your service endpoint by adding descriptive information to your SAML 
configuration. This will be used when generating metadata, see 
[pysaml2 docs](https://pysaml2.readthedocs.io/en/latest/howto/config.html#configuration-directives) for a full list of 
attributes.

```py
SAML_CONFIG = {
    # extra configuration removed for clarity
    
    'name': 'My custom application.',
    
    'description': 'My custom application does something rad.',
    
    'organization': {
        'name': [
            ('Example Organisation', 'en'),
            ('Primjer Organizacije', 'hr')
        ],
        'display_name': ['Primjer Organizacije'],
        'url': [
            ('http://example.org', 'en'),
            ('http://hr.example.org', 'hr'),
        ],
    },
    
    'contact_person': [
        {
            'given_name': 'Fox',
            'sur_name': 'Mulder',
            
            'company': 'The X-Files',
            'email_address': ['fmulder@xfiles.com'],
            'telephone_number': ['+1 234 567 89'],

            # accepted values: technical, support, administrative, billing and other
            'contact_type': 'technical',

        },
        {
            'given_name': 'Dana',
            'sur_name': 'Scully',
            
            'company': 'The X-Files',
            'email_address': ['dscully@xfiles.com'],
            'telephone_number': ['123-456-789'],
            
            'contact_type': 'administrative',
        },
    ],
}
```

## Resource type

After everything else has been configured, you will need to toggle AAI@EduHr resource from test to production. First
update the AAI@EduHr metadata URL in the `SAML_CONFIG`. Test and production URLs are documented in the 
official [AAI@EduHr documentation](https://wiki.srce.hr/spaces/AAIUPUTE/pages/69501694/SAML+metapodaci+SSO+servisa).

```py
SAML_CONFIG = {
    # extra configuration removed for clarity
    
    'metadata': {
        'remote': [
            {
                'url': 'https://login.aaiedu.hr/sso/saml2/idp/metadata.php',
            }
        ]
    },
}
```

Finally, toggle the *Resource Type* from `Test` to `Produkcija` in the resource registry.
