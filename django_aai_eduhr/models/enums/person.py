"""
Choice enums corresponding to values defined in hrEduPerson scheme ver. 1.3.1.

https://wiki.srce.hr/download/attachments/65405172/AAI@EduHr-hrEduSheme-2010-v1.3.1.pdf?version=1&modificationDate=1727940424000&api=v2
"""
from django.db import models
from django.utils.translation import gettext as _


class Affiliation(models.TextChoices):
    """hrEduPersonPrimaryAffiliation and hrEduPersonAffiliation enum."""
    LIFELONG_EDUCATION = 'cjeloživotno obrazovanje', _('Lifelong Education')
    EMPLOYEE = 'djelatnik', _('Employee')
    GUEST = 'gost', _('Guest')
    SERVICE_USER = 'korisnik usluge', _('Service User')
    STUDENT = 'student', _('Student')
    PUPIL = 'učenik', _('Pupil')
    EXTERNAL_ASSOCIATE = 'vanjski suradnik', _('External Associate')


class AcademicStatus(models.TextChoices):
    """hrEduPersonAcademicStatus enum."""
    ASSISTANT = 'asistent', _('Assistant')
    ASSISTANT_LECTURER = 'asistent - predavač', _('Assistant Lecturer')
    ASSISTANT_PROFESSOR = 'docent', _('Assistant Professor')
    ASSOCIATE_PROFESSOR = 'izvanredni profesor', _('Associate Professor')
    LIBRARIAN = 'knjižničar', _('Librarian')
    ACCOMPANIST = 'korepetitor', _('Accompanist')
    LECTURER = 'lektor', _('Lecturer')
    LECTURE_VERIFICATION = 'povjera predavanja', _('Lecture Verification')
    LECTURER_GENERAL = 'predavač', _('Lecturer')
    COLLEGE_PROFESSOR = 'profesor visoke škole', _('College Professor')
    FULL_PROFESSOR = 'redoviti profesor', _('Full Professor')
    PROFESSIONAL_ASSOCIATE = 'stručni suradnik', _('Professional Associate')
    ARTISTIC_ASSOCIATE = 'umjetnički suradnik', _('Artistic Associate')
    SENIOR_ASSISTANT = 'viši asistent', _('Senior Assistant')
    SENIOR_LIBRARIAN = 'viši knjižničar', _('Senior Librarian')
    SENIOR_ACCOMPANIST = 'viši korepetitor', _('Senior Accompanist')
    SENIOR_LECTURER = 'viši lektor', _('Senior Lecturer')
    SENIOR_LECTURER_GENERAL = 'viši predavač', _('Senior Lecturer')
    SENIOR_ARTISTIC_ASSOCIATE = 'viši umjetnički suradnik', _('Senior Artistic Associate')
    SENIOR_SCIENTIFIC_ASSOCIATE = 'viši znanstveni suradnik', _('Senior Scientific Associate')
    JUNIOR_RESEARCHER = 'znanstveni novak', _('Junior Researcher')
    SCIENTIFIC_ADVISOR = 'znanstveni savjetnik', _('Scientific Advisor')
    SCIENTIFIC_ASSOCIATE = 'znanstveni suradnik', _('Scientific Associate')


class Gender(models.IntegerChoices):
    """hrEduPersonGender enum."""
    UNKNOWN = 0, _('Unknown')
    MALE = 1, _('Male')
    FEMALE = 2, _('Female')
    NOT_GIVEN = 9, _('Not given')


class ProfessionalStatus(models.TextChoices):
    """hrEduPersonProfessionalStatus enum."""
    DOCTOR_OF_SCIENCE = 'dr.sc.', _('Doctor of Science')
    QUALIFIED_WORKER = 'KV', _('Qualified Worker')
    MASTER_ENGINEER_PROFESSIONAL_DOCTOR = (
        'magistar / magistar inženjer / doktor struke', _('Master / Engineer / Professional Doctor')
    )
    MASTER_OF_SCIENCE = 'mr.sc.', _('Master of Science')
    UNSKILLED_WORKER = 'NKV', _('Unskilled Worker')
    ELEMENTARY_EDUCATION = 'NSS', _('Elementary Education')
    PARTIALLY_QUALIFIED_WORKER = 'PKV', _('Partially Qualified Worker')
    SECONDARY_EDUCATION = 'SSS', _('Secondary Education')
    PROFESSIONAL_ASSOCIATE = 'stručni pristupnik', _('Professional Associate')
    PROFESSIONAL_BACHELOR_ENGINEER = (
        'stručni prvostupnik / prvostupnik inženjer', _('Professional Bachelor / Bachelor Engineer')
    )
    PROFESSIONAL_SPECIALIST_ENGINEER_MEDICAL_GRADUATE = (
        'stručni specijalist / stručni specijalist inženjer / diplomirani medicinske struke',
        _('Professional Specialist / Specialist Engineer / Medical Graduate')
    )
    UNIVERSITY_BACHELOR_ENGINEER = (
        'sveučilišni prvostupnik / prvostupnik inženjer', _('University Bachelor / Bachelor Engineer')
    )
    UNIVERSITY_SPECIALIST_MASTER = (
        'sveučilišni specijalist / sveučilišni magistar', _('University Specialist / University Master')
    )
    HIGHLY_QUALIFIED_WORKER = 'VKV', _('Highly Qualified Worker')
    HIGHER_EDUCATION = 'VS', _('Higher Education')
    UNIVERSITY_DEGREE = 'VSS', _('University Degree')
    ASSOCIATE_DEGREE = 'VŠS', _('Associate Degree')


class Role(models.TextChoices):
    """hrEduPersonRole enum."""
    DIRECTORY_ADMINISTRATOR = 'administrator imenika', _('Directory Administrator')
    CARNET_COORDINATOR = 'CARNet koordinator', _('CARNet Coordinator')
    CARNET_SYSTEM_ENGINEER = 'CARNet sistem inženjer', _('CARNet System Engineer')
    ICT_COORDINATOR = 'ICT koordinator', _('ICT Coordinator')
    ISVU_COORDINATOR = 'ISVU koordinator', _('ISVU Coordinator')
    ICT_SECURITY_CONTACT = 'kontakt za sigurnosna pitanja u području ICT', _('ICT Security Contact')
    MATICA_OPERATOR = 'MATICA operater', _('MATICA Operator')
    MATICA_EDITOR = 'MATICA urednik', _('MATICA Editor')
    MS_COORDINATOR = 'MS koordinator', _('MS Coordinator')


class StaffCategory(models.TextChoices):
    """hrEduPersonStaffCategory enum"""
    ADMINISTRATIVE_STAFF = 'administrativno osoblje', _('Administrative Staff')
    ICT_SUPPORT = 'ICT podrška', _('ICT Support')
    RESEARCHERS = 'istraživači', _('Researchers')
    TEACHING_STAFF = 'nastavno osoblje', _('Teaching Staff')
    LIBRARY_STAFF = 'osoblje knjižnice', _('Library Staff')
    TECHNICAL_STAFF = 'tehničko osoblje', _('Technical Staff')


class StudentCategory(models.TextChoices):
    """hrEduPersonStudentCategory enum."""
    PART_TIME_MASTER_STUDENT = (
        'izvanredni student:diplomski sveučilišni studij', _('Part-Time Student: University Master Study')
    )
    PART_TIME_DOCTORAL_STUDENT = 'izvanredni student:doktorski studij', _('Part-Time Student: Doctoral Study')
    PART_TIME_INTEGRATED_STUDENT = 'izvanredni student:integrirani studij', _('Part-Time Student: Integrated Study')
    PART_TIME_PRE_BOLOGNA_STUDENT = (
        'izvanredni student:pred-bolonjski studij', _('Part-Time Student: Pre-Bologna Study')
    )
    PART_TIME_BACHELOR_TECHNICIAN_STUDENT = (
        'izvanredni student:preddiplomski stručni studij', _('Part-Time Student: Professional Bachelor Study')
    )
    PART_TIME_BACHELOR_STUDENT = (
        'izvanredni student:preddiplomski sveučilišni studij', _('Part-Time Student: University Bachelor Study')
    )
    PART_TIME_SPECIALIST_STUDENT = (
        'izvanredni student:specijalistički diplomski stručni studij', _('Part-Time Student: Specialist Master Study')
    )
    PART_TIME_POSTGRADUATE_SPECIALIST = (
        'izvanredni student:specijalistički poslijediplomski studij',
        _('Part-Time Student: Specialist Postgraduate Study')
    )
    STUDENT_LEAVE_OF_ABSENCE = 'mirovanje statusa studenta', _('Student Leave of Absence')
    ELEMENTARY_SCHOOL_STUDENT = 'osnovnoškolac', _('Elementary School Student')
    FULL_TIME_MASTER_STUDENT = (
        'redoviti student:diplomski sveučilišni studij', _('Full-Time Student: University Master Study')
    )
    FULL_TIME_DOCTORAL_STUDENT = 'redoviti student:doktorski studij', _('Full-Time Student: Doctoral Study')
    FULL_TIME_INTEGRATED_STUDENT = 'redoviti student:integrirani studij', _('Full-Time Student: Integrated Study')
    FULL_TIME_PRE_BOLONJA_STUDENT = 'redoviti student:pred-bolonjski studij', _('Full-Time Student: Pre-Bologna Study')
    FULL_TIME_BACHELOR_TECHNICIAN_STUDENT = (
        'redoviti student:preddiplomski stručni studij',
        _('Full-Time Student: Professional Bachelor Study')
    )
    FULL_TIME_BACHELOR_STUDENT = (
        'redoviti student:preddiplomski sveučilišni studij',
        _('Full-Time Student: University Bachelor Study')
    )
    FULL_TIME_SPECIALIST_STUDENT = (
        'redoviti student:specijalistički diplomski stručni studij',
        _('Full-Time Student: Specialist Master Study')
    )
    FULL_TIME_POSTGRADUATE_SPECIALIST = (
        'redoviti student:specijalistički poslijediplomski studij',
        _('Full-Time Student: Specialist Postgraduate Study')
    )
    HIGH_SCHOOL_STUDENT = 'srednjoškolac', _('High School Student')


class Title(models.TextChoices):
    """hrEduPersonTitle enum."""
    DEAN = 'dekan', _('Dean')
    DIRECTOR = 'direktor', _('Director')
    ASSISTANT_DIRECTOR = 'pomoćnik ravnatelja', _('Assistant Director')
    DEPARTMENT_HEAD = 'predstojnik zavoda', _('Department Head')
    CHAIR_HEAD = 'pročelnik katedre', _('Chair Head')
    SECTION_HEAD = 'pročelnik odsjeka', _('Section Head')
    UNIVERSITY_DEPARTMENT_HEAD = 'pročelnik sveučilišnog odjela', _('University Department Head')
    VICE_DEAN = 'prodekan', _('Vice Dean')
    VICE_RECTOR = 'prorektor', _('Vice Rector')
    PRINCIPAL = 'ravnatelj', _('Principal')
    RECTOR = 'rektor', _('Rector')
    LAB_MANAGER = 'voditelj laboratorija', _('Laboratory Manager')
    DEPARTMENT_MANAGER = 'voditelj odjela', _('Department Manager')
    UNIT_MANAGER = 'voditelj organizacijske jedinice', _('Organizational Unit Manager')
    PROJECT_MANAGER = 'voditelj projekta', _('Project Manager')
    DEPUTY_UNIVERSITY_DEPARTMENT_HEAD = (
        'zamjenik pročelnika sveučilišnog odjela', _('Deputy University Department Head')
    )
    DEPUTY_DIRECTOR = 'zamjenik ravnatelja', _('Deputy Director')
