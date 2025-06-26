import logging

import dateutil.parser
import djangosaml2.backends
from django.apps import apps
from django.conf import settings
from django.core import exceptions
from django.core.cache import caches
from django.utils import timezone

import django_aai_eduhr.signals

logger = logging.getLogger(__name__)


class AssertionReplayMitigationMixin:
    """Mitigates Assertion Replay Attack by validating `NotOnOrAfter` attribute and storing used assertions in cache
    until `NotOnOrAfter`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            name = settings.AAI_ASSERTION_CACHE
        except AttributeError:
            name = 'default'

        self.cache = caches[name]

    def is_authorized(self, attributes, attribute_mapping, idp_entityid, assertion_info, **kwargs):
        """
        Verifies cached assertion id and `NotOnOrAfter` attribute.

        Parameters
        ----------
        attributes: dict
        attribute_mapping: dict
        idp_entityid: str
        assertion_info: dict
        **kwargs: dict

        Returns
        -------
        allowed : bool
        """

        allowed = super().is_authorized(attributes, attribute_mapping, idp_entityid, assertion_info, **kwargs)
        if assertion_info:
            assertion_id = assertion_info.get('assertion_id')

            now = timezone.datetime.now(timezone.utc)
            not_on_or_after = dateutil.parser.parse(assertion_info.get('not_on_or_after'))
            expiration = not_on_or_after - now

            if expiration.total_seconds() <= 0:
                allowed = False
            else:
                if self.cache.get(assertion_id):
                    logger.info('Received assertion has been already used.')
                    allowed = False
                else:
                    self.cache.set(assertion_id, 'True', expiration)

        return allowed


class AAIBackend(AssertionReplayMitigationMixin, djangosaml2.backends.Saml2Backend):
    """Ready to use authentication backend which supports basic authorisation."""

    def _update_user(self, user, attributes, attribute_mapping, force_save=False):
        """
        Sends AAI update signals, sets AAI data on the user instance, and calls `self._update_aai_data` to update
        `AAI_MODEL` with the retrieved data.

        Parameters
        ----------
        user : django.contrib.auth.models.User
        attributes : dict
        attribute_mapping : dict
        force_save : bool

        Returns
        -------
        user: django.contrib.auth.models.User
        """

        django_aai_eduhr.signals.aai_pre_update.send(type(self), user=user)
        user = super()._update_user(user, attributes, attribute_mapping, force_save)

        if hasattr(settings, 'AAI_MODEL') and settings.AAI_MODEL:
            self._update_aai_data(user, attributes, attribute_mapping)
        else:
            logger.warning(
                '"AAI_MODEL" is not present in the settings. '
                "Make sure you it is configured if you are storing data in a related model."
            )

        django_aai_eduhr.signals.aai_post_update.send(type(self), user=user)
        return user

    def _update_aai_data(self, user, attributes, attribute_mapping):
        """
        Create or update existing `AAI_MODEL` with the data retrieved from the IdP.

        Parameters
        ----------
        user : django.contrib.auth.models.User
        attributes : dict
        attribute_mapping : dict
        """

        username = getattr(user, user.USERNAME_FIELD)
        if not hasattr(user, settings.AAI_MODEL_RELATED_NAME):
            logger.info(f'Creating AAI Data model for user {username}.')
            aai = self._create_aai_data(user)
        else:
            logger.info(f'Fetching AAI Data model for user {username}.')
            aai = self._get_aai_data(user)

        for saml_attribute, user_attributes in attribute_mapping.items():
            if len(user_attributes) == 0:
                raise exceptions.ImproperlyConfigured(f'Attribute "{saml_attribute}" is not mapped to model field.')

            if saml_attribute not in attributes:
                # It seems that AAI@EduHR Lab does not send some attributes.
                error = f'Attribute "{saml_attribute}" not received or is not present in SAML attribute map.'
                if not settings.DEBUG:
                    raise exceptions.ImproperlyConfigured(error)
                else:
                    logger.warning(error)
            else:
                for user_attribute in user_attributes:
                    if self._is_aai_relation(user_attribute):
                        # discard AAI MODEL qualifier.
                        user_attribute = user_attribute[len(settings.AAI_MODEL_RELATED_NAME) + 1:]

                        attribute_values = attributes[saml_attribute]
                        obj, attr, value, child_attr = self._get_nested_attribute(aai, user_attribute)
                        if child_attr:  # attr is relation
                            self._set_related_values(aai, user_attribute, attribute_values)
                        else:
                            self._set_nested_value(aai, user_attribute, attribute_values[0])

        if aai:
            aai.save()

    def _get_aai_model(self):
        """
        Retrieve `AAI_MODEL` type from the settings.

        Returns
        -------
        model : subclass of django.db.models.Model
        """
        try:
            app, model = settings.AAI_MODEL.split('.')
            return apps.get_model(app, model)
        except ValueError:
            raise exceptions.ImproperlyConfigured('"AAI_MODEL" setting must be in the format "<app>.<model>".')

    def _get_aai_data(self, user):
        """
        Retrieve `AAI_MODEL` related to the user.

        Parameters
        ----------
        user: django.contrib.auth.models.User

        Returns
        -------
        aai_instance : django.models.Model
        """
        return self._get_aai_model().objects.get(user=user)

    def _create_aai_data(self, user):
        """
        Create `AAI_MODEL` related to the user.

        Parameters
        ----------
        user: django.contrib.auth.models.User

        Returns
        -------
        model : django.contrib.models.Model
        """
        return self._get_aai_model().objects.create(user=user)

    @staticmethod
    def _is_aai_relation(attribute):
        """
        Determine if an attribute matches `AAI_MODEL_RELATED_NAME`. Attribute can be nested, e.g.
        `attribute.sub_attr1.sub_attr2` in which case only `attribute` is checked.

        Parameters
        ----------
        attribute: str

        Returns
        -------
        is_aai_relation : bool
        """

        attribute = attribute.split('.')[0]
        return attribute == settings.AAI_MODEL_RELATED_NAME

    @classmethod
    def _is_relation(cls, obj, attribute):
        """
        Determine if an attribute is a reverse side of a ForeignKey relation. Attribute can be nested, e.g.
        `attribute.sub_attr1.sub_attr2` in which case only the `attribute` is checked.

        Parameters
        ----------
        obj: object
        attribute: str

        Returns
        -------
        is_relation : bool
        """

        relation = False
        if attribute.isidentifier() and hasattr(obj, attribute):
            manager = getattr(obj, attribute)
            relation = hasattr(manager, 'field') and manager.field.is_relation

        return relation

    @classmethod
    def _get_nested_attribute(cls, obj, attribute):
        """Traverses nested attributes returning tuple of (nested_obj, attribute, value, child_attribute)."""
        links = attribute.split('.')
        current_obj = obj
        current_attr = attr = links[0]
        child_attr = ''
        value = None
        for i, attr in enumerate(links):
            if i > 0:
                current_attr = f'{current_attr}.{attr}'

            if not attr.isidentifier():
                raise NameError(
                    f'"{attr}" is not a valid identifier, invalid attribute specification in '
                    f'"{obj.__class__}.{current_attr}".'
                )

            if not hasattr(current_obj, attr):
                raise AttributeError(
                    f'"{current_obj}" does not have the attribute "{attr}", '
                    f'invalid attribute specification in "{obj.__class__}.{current_attr}".'
                )

            if cls._is_relation(current_obj, attr):
                try:
                    child_attr = links[i + 1]
                    value = getattr(current_obj, attr)

                    if not child_attr.isidentifier():
                        raise NameError(
                            f'"{child_attr}" is not a valid identifier, invalid attribute '
                            f'specification in relation "{obj.__class__}.{current_attr}".'
                        )

                    break
                except IndexError:
                    raise exceptions.ImproperlyConfigured(
                        f'"{obj.__class__}.{current_attr}" is a relation, '
                        'but related object attribute is not specified.'
                    )
            else:
                value = getattr(current_obj, attr)

                if i < len(links) - 1:
                    current_obj = value

        return current_obj, attr, value, child_attr

    @classmethod
    def _get_nested_value(cls, obj, attribute):
        """
        Returns value of a nested attribute.

        Parameters
        ----------
        obj: object
        attribute: str

        Returns
        -------
        value: object
        """

        _, _, value, _ = cls._get_nested_attribute(obj, attribute)
        return value

    @classmethod
    def _get_related_values(cls, obj, attribute):
        """
        Returns QuerySet of related objects for an attribute which is a (nested) relation.

        Parameters
        ----------
        obj: object
        attribute: str

        Returns
        -------
        related_values: django.models.db.QuerySet
        """

        target, attr, related, child_attr = cls._get_nested_attribute(obj, attribute)
        if not child_attr:
            raise ValueError(f'"{target.__class__}.{attr}" is not a relation.')

        return related.all()

    @classmethod
    def _set_nested_value(cls, obj, attribute, value):
        """
        Set value of a nested attribute.

        Parameters
        ----------
        obj: object
        attribute: str
        value: object
        """
        target, attr, _, _ = cls._get_nested_attribute(obj, attribute)
        setattr(target, attr, value)

    @classmethod
    def _set_related_values(cls, obj, attribute, values):
        """
        Bulk create related objects for an attribute which is a (nested) relation.

        Parameters
        ----------
        obj: object
        attribute: str
        values: object
        """

        target, attr, related, child_attr = cls._get_nested_attribute(obj, attribute)
        if not child_attr:
            raise ValueError(f'"{target.__class__}.{attribute}" is not a relation.')

        related.all().delete()
        to_create = [
            related.model(**{child_attr: value, related.field.name: related.instance})
            for value in values
        ]
        related.bulk_create(to_create)

    def is_authorized(self, attributes, attribute_mapping, idp_entityid, assertion_info, **kwargs):
        """
        Verify if user is authorised by comparing attribute values in `AAI_BACKEND_AUTHORISATION` based on
        configured `AAI_BACKEND_POLICY`.

        Parameters
        ----------
        attributes: dict
        attribute_mapping: dict
        idp_entityid: str
        assertion_info: dict
        **kwargs: dict

        Returns
        -------
        allowed : bool
        """
        try:
            authorised_attributes = settings.AAI_BACKEND_AUTHORISATION
        except AttributeError:
            authorised_attributes = dict()

        # skip if not defined
        allowed = len(authorised_attributes.keys()) < 1
        if not allowed:
            try:
                policy = settings.AAI_BACKEND_POLICY
            except AttributeError:
                policy = 'all'

            tests = []
            for attribute, values in authorised_attributes.items():
                if attribute not in attributes:
                    tests.append(False)
                else:
                    tests.append(attributes[attribute] == values)

            allowed = all(tests) if policy == 'all' else any(tests)

        return allowed
