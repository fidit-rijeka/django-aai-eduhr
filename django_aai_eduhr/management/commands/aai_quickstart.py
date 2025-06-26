import importlib
import inspect
import io
import os
import pathlib
import pprint
import shutil

from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _


class Command(BaseCommand):
    help = _('Generates quickstart settings for AAI@EduHr integration.')

    def _boolean_input(self, default):
        accepted = ('y', 'n', '')
        value_map = {
            'y': True,
            'n': False
        }

        if default not in value_map.keys():
            raise ValueError('default value is not one of the accepted values.')

        value = '/'
        while value.lower() not in accepted:
            value = input(f'Default: {default} (y/n): ')

        value = default if value == '' else value
        return value_map[value]

    def _str_input(self, default):
        value = input(f'Default: {default}: ')
        value = default if value == '' else value
        return value

    def _pretty_print(self, obj):
        buffer = io.StringIO()
        pprint.pprint(obj, stream=buffer)
        return buffer.getvalue()

    def _write_config(self, output_path, data):
        with open(output_path, 'r+') as f:
            contents = f.read()

            if contents.endswith('\n'):
                contents += '\n'
            else:
                contents += '\n\n'

            contents += data

            f.seek(0)
            f.write(contents)

    def _path_placeholder(self):
        return '/dev/null' if os.name != 'nt' else 'NUL'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--output', help=_('Path where to output generated settings.'))
        parser.add_argument('-w', '--overwrite', action='store_true', help=_('Overwrite current settings.'))

    def handle(self, *args, **options):
        settings_dir = os.environ.get('DJANGO_SETTINGS_MODULE')
        if settings_dir is not None:
            settings_file = inspect.getfile(importlib.import_module(settings_dir))
            settings_dir = pathlib.Path(settings_file).parent

            self.stdout.write(
                _(
                    '\nThis wizard will help you generate a starting point AAI@EduHr configuration '
                    'so you can dive into development right away.'
                )
            )
            self.stdout.write(
                self.style.WARNING(_('These settings are not considered optimal and are not suitable for production.'))
            )

            self.stdout.write(_('\nContinue?'))
            go_next = self._boolean_input('y')

            if go_next:
                self.stdout.write(_('\nEnable SAML debug mode? This is useful for retrieving logs during development.'))
                saml_debug = self._boolean_input('y')

                xmlsec1 = shutil.which('xmlsec12')
                if not xmlsec1:
                    self.stdout.write(
                        self.style.ERROR(
                            _('\nXML Security Library not found. This is required for SAML operations. '
                                'Enter the path to the xmlsec1 binary.')
                        )
                    )
                    xmlsec1 = self._str_input(self._path_placeholder())
                else:
                    self.stdout.write(
                        _('\nXML Security Library found at "%(xmlsec)s". '
                          'You can enter alternative path to the xmlsec1 binary if you wish.') % {'xmlsec': xmlsec1}
                    )
                    xmlsec1 = self._str_input(xmlsec1)

                self.stdout.write(
                    _('\nUse AAI@EduHr Lab? This is a sandbox environment for developing and testing '
                      'AAI@EduHr applications, but will have to be changed for production.')
                )
                use_fedlab = self._boolean_input('y')

                self.stdout.write(_('\nEnter base URL your application is served from, excluding trailing slash.'))
                base_url = self._str_input('http://localhost:8000')

                self.stdout.write(
                    _('\nDoes the application require IdP assertions to be signed? This is recommended in production, '
                      'but "Sign Assertions" needs to be enabled in the resource registry.')
                )
                signed_assertions = self._boolean_input('n')

                self.stdout.write(
                    _('\nDoes the application require IdP responses to be signed? This is recommended in production, '
                      'but "Sign Response" needs to be enabled in the resource registry.')
                )
                signed_responses = self._boolean_input('n')

                self.stdout.write(
                    _('\nDoes the application sign authn requests? This is recommended in production, but '
                      '"Validate Logout Requests" needs to be enabled in the resource registry.')
                )
                sign_authn = self._boolean_input('n')

                self.stdout.write(
                    _('\nDoes the application sign logout requests? This is recommended in production, but '
                      '"Validate Logout Requests" needs to be enabled in the resource registry.')
                )
                sign_logout = self._boolean_input('n')

                self.stdout.write(
                    _('\nDoes the application force authentication? This will ignore previously established SSO '
                      'sessions, and will require clients to log in every time.')
                )
                force_authn = self._boolean_input('n')

                self.stdout.write(
                    _('\nDoes the application allow unsolicited responses? This will process SAML responses for which '
                      'the application did not send out corresponding request.')
                )
                allow_unsolicited = self._boolean_input('n')

                security = any([signed_assertions, signed_responses, sign_authn, sign_logout])
                if security:
                    self.stdout.write(
                        _('\nEnter the path to the PEM formatted file that contains the private key of the service. '
                          'This will be used to sign/encrypt communication between SP and IdP.')
                    )
                    key_file = self._str_input(self._path_placeholder())

                    self.stdout.write(
                        _('\nEnter the path to the PEM formatted file that contains the certificate of the service. '
                          'This will be used to sign/encrypt communication between SP and IdP.')
                    )
                    cert_file = self._str_input(self._path_placeholder())

                    self.stdout.write(
                        self.style.WARNING(
                            _('\n not forget to configure encryption and/or '
                              'signing certificate in the resource registry.')
                        )
                    )

                if use_fedlab:
                    metadata_url = 'https://fed-lab.aaiedu.hr/sso/saml2/idp/metadata.php'
                else:
                    metadata_url = 'https://login.aaiedu.hr/sso/saml2/idp/metadata.php'

                imports = 'import saml2'
                bindings = (
                    'SAML_DEFAULT_BINDING = saml2.BINDING_HTTP_POST\n'
                    'SAML_LOGOUT_REQUEST_PREFERRED_BINDING = saml2.BINDING_HTTP_REDIRECT'
                )

                saml_config = {
                    'debug': saml_debug,

                    'xmlsec_binary': xmlsec1,
                    'crypto_backend': 'xmlsec1',

                    'entityid': '{}/aai/metadata/'.format(base_url),

                    'service': {
                        'sp': {
                            'endpoints': {
                                'assertion_consumer_service': ['{}/aai/acs/'.format(base_url)],
                                'single_logout_service': ['{}/aai/ls/'.format(base_url)],
                            },

                            'want_assertions_signed': signed_assertions,
                            'want_response_signed': signed_responses,

                            'logout_requests_signed': sign_logout,
                            'logout_responses_signed': sign_logout,
                            'authn_requests_signed': sign_authn,

                            'force_authn': force_authn,

                            'allow_unsolicited': allow_unsolicited
                        },
                    },

                    'metadata': {
                        'remote': [
                            {
                                'url': metadata_url,
                            }
                        ]
                    },

                    'attribute_map_dir': str(settings_dir)
                }

                if security:
                    saml_config['key_file'] = key_file
                    saml_config['cert_file'] = cert_file

                    saml_config['encryption_keypairs'] = [{
                        'key_file': key_file,
                        'cert_file': cert_file
                    }]

                app_dir = pathlib.Path(apps.get_app_config('django_aai_eduhr').path)
                cpy_src = app_dir / 'aai_attribute_map.py'
                cpy_target = settings_dir / 'aai_attribute_map.py'
                self.stdout.write(
                    _('\nCopying SAML attribute map to %(attribute_map)s.') % {'attribute_map': cpy_target}
                )
                shutil.copy(cpy_src, cpy_target)

                data = (
                    f'{imports}\n\n'
                    f'{bindings}\n\n'
                    f'SAML_CONFIG = {self._pretty_print(saml_config)}'
                )

                if options['overwrite']:
                    self._write_config(settings_file, data)
                else:
                    if options['output']:
                        quickstart_settings = options['output']
                    else:
                        quickstart_settings = settings_dir / 'quickstart_settings.py'

                    shutil.copy(settings_file, quickstart_settings)
                    self._write_config(quickstart_settings, data)

                    self.stdout.write(
                        self.style.SUCCESS(
                            _('\nGenerated AAI@EduHR SAML configuration at %(path)s.') % {'path': quickstart_settings}
                        )
                    )
                    self.stdout.write(
                        self.style.WARNING(
                            _("Don't forget to complete the remaining necessary configuration, "
                              "see the documentation for more details.")
                        )
                    )
        else:
            self.stdout.write(
                self.style.ERROR(
                    'Unable to find settings module. Please verify if '
                    'DJANGO_SETTINGS_MODULE envar is correctly configured.'
                )
            )
