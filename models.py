from email.policy import default
from django.db import models


# Create your models here.


class batch(models.Model):
    class_name = models.CharField(max_length=255)
    date_of_join = models.DateField(null=True)
    semester = models.CharField(max_length=255)
    scheme = models.BigIntegerField(null=False)
    tutor_id = models.BigIntegerField(null=False, default=0)

    def __str__(self):
        name = self.class_name + " S-" + self.semester
        return name


class scheme(models.Model):
    scheme = models.CharField(max_length=255, null=False)

    def __str__(self):
        name = self.scheme
        return name


class subject(models.Model):
    code = models.CharField(max_length=255, null=False)
    subject_name = models.CharField(max_length=255, null=False)
    credit = models.BigIntegerField(null=False)
    scheme = models.BigIntegerField(null=False)

    def __str__(self):
        name = self.code + "-" + self.subject_name
        return name


class subject_to_staff(models.Model):
    subject_id = models.BigIntegerField(null=False)
    batch_id = models.BigIntegerField(null=False)
    staff_id = models.BigIntegerField(null=False)
    semester = models.BigIntegerField(null=False)

    def __str__(self):
        name = self.subject_id
        return name


class semester_result(models.Model):
    university_no = models.CharField(max_length=255, null=False, unique=False)
    subject_id = models.BigIntegerField(null=False)
    grade_point = models.FloatField(null=False)
    semester = models.BigIntegerField(null=False)
    batch_id = models.BigIntegerField(null=False)
    month = models.BigIntegerField(null=False)
    year = models.BigIntegerField(null=False)
    no_of_chances = models.BigIntegerField(null=False)
