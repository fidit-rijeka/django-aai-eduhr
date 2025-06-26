from django.db import models

from django_aai_eduhr.models.enums import org


class OrganisationTypeField(models.CharField):
    """Field with hrEduOrgType choices."""
    def __init__(self, *args, **kwargs):
        kwargs.pop('choices')
        super().__init__(*args, choices=org.OrganisationType.choices, **kwargs)
