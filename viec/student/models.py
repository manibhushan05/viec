from django.db import models

from utils.models import Country, Address, Language


class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE')
    )
    MARITAL_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
    )
    first_name = models.CharField(max_length=50, null=True)
    middle_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    date_of_birth = models.DateField(null=True)
    first_language = models.CharField(max_length=100, null=True)  # bad choice, pls make language table
    citizenship = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    passport_number = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=1, null=True)
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    education_gap = models.CharField(max_length=200, null=True)
    previous_visited_consultant = models.CharField(max_length=200, null=True)
    refusal_country = models.ForeignKey(Country, related_name='refusal_country', on_delete=models.CASCADE)
    dependent = models.CharField(max_length=200, null=True)
    remarks = models.CharField(max_length=500, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)


class Application(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    apply_date = models.DateField(null=True)
    program = models.CharField(max_length=200, null=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.DO_NOTHING)
    institution = models.CharField(max_length=300, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)


class EducationLevel(models.Model):
    CATEGORY_CHOICES = (
        ('PR', 'Primary'),
        ('SR', 'Secondary'),
        ('UG', 'Under Graduate'),
        ('PG', 'Post Graduate')
    )
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=2)
    active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)


class Institution(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    level_of_education = models.ForeignKey(EducationLevel, on_delete=models.DO_NOTHING)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    institute_name = models.CharField(max_length=200, null=True)
    medium_of_instruction = models.ForeignKey(Language, null=True, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    degree_awarded = models.CharField(max_length=100, null=True)
    marks = models.CharField(max_length=20, null=True, help_text='Enter Grade/Marks')
    degree_awarded_on = models.DateField()
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)


class AdditionalQualification(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    EXAM_CATEGORY = (
        ('GRE', 'GRE'),
        ('GMAT', 'GMAT'),
        ('IELTS', 'IELTS'),
        ('TOFEL', 'TOFEL'),
        ('PTE', 'PTE')
    )
    exam_date = models.DateField()

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)


class Score(models.Model):
    name = models.CharField(max_length=50, null=True)
    marks = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    additional_qualification = models.ForeignKey(AdditionalQualification, null=True, on_delete=models.CASCADE)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)


class Experience(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    mode_of_salary = models.CharField(max_length=20, null=True)
    job_description = models.CharField(max_length=500, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)
