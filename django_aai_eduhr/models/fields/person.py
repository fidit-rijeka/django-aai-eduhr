from django.db import models

from django_aai_eduhr.models.enums import person


class AffiliationField(models.CharField):
    """Field with hrEduPersonPrimaryAffiliation and hrEduPersonAffiliation choices."""
    def __init__(self, *args, **kwargs):
        kwargs.pop('choices')
        super().__init__(*args, choices=person.Affiliation.choices, **kwargs)


class AcademicStatusField(models.CharField):
    """Field with hrEduPersonAcademicStatus choices."""
    def __init__(self, *args, **kwargs):
        kwargs.pop('choices', None)
        super().__init__(*args, choices=person.AcademicStatus.choices, **kwargs)


class GenderField(models.IntegerField):
    """Field with hrEduPersonGender choices."""
    def __init__(self, *args, **kwargs):
        kwargs.pop('choices', None)
        super().__init__(*args, choices=person.Gender.choices, **kwargs)


class ProfessionalStatusField(models.CharField):
    """Field with hrEduPersonProfessionalStatus choices."""
    def __init__(self, *args, **kwargs):
        kwargs.pop('choices', None)
        super().__init__(*args, choices=person.ProfessionalStatus.choices, **kwargs)


class RoleField(models.CharField):
    """Field with hrEduPersonRole choices."""
    def __init__(self, *args, **kwargs):
        kwargs.pop('choices', None)
        super().__init__(*args, choices=person.Role.choices, **kwargs)


class StaffCategoryField(models.CharField):
    """Field with hrEduPersonStaffCategory choices."""
    def __init__(self, *args, **kwargs):
        kwargs.pop('choices', None)
        super().__init__(*args, choices=person.StaffCategory.choices, **kwargs)


class StudentCategoryField(models.CharField):
    """Field with hrEduPersonStudentCategory choices."""
    def __init__(self, *args, **kwargs):
        kwargs.pop('choices', None)
        super().__init__(*args, choices=person.StudentCategory.choices, **kwargs)


class TitleField(models.CharField):
    """Field with hrEduPersonTitle choices."""
    def __init__(self, *args, **kwargs):
        kwargs.pop('choices', None)
        super().__init__(*args, choices=person.Title.choices, **kwargs)
