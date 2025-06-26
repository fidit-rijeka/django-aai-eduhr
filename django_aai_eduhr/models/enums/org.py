from django.db import models


class OrganisationType(models.TextChoices):
    """hrEduOrgType enum."""

    OTHER_LEGAL_ENTITIES = 'Druge pravne osobe'
    FACULTY = 'Fakultet'
    PUBLIC_SCIENTIFIC_INSTITUTE = 'Javni znanstveni institut'
    LIBRARY = 'Knjižnica'
    ELEMENTARY_SCHOOL = 'Osnovna škola'
    PRIVATE_SCHOOL = 'Privatna visoka škola s pravom javnosti'
    HIGH_SCHOOL = 'Srednja škola'
    STUDENT_CENTER = 'Studentski centar'
    UNIVERSITY_DEPARTMENT = 'Sveučilišni odjel'
    UNIVERSITY_PROGRAM = 'Sveučilišni studij'
    UNIVERSITY = 'Sveučilište'
    ART_ACADEMY = 'Umjetnička akademija'
    SIGNIFICANT_INSTITUTION = 'Ustanova od posebnog značaja za Republiku Hrvatsku'
    POLYTECHNIC = 'Veleučilište'
    COLLEGE = 'Visoka škola'
    SCIENTIFIC_INSTITUTE = 'Znanstveni institut'
