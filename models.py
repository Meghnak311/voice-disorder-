import email
from django.db import models

# Create your models here.
from login.models import MyUser


class profile_student(models.Model):
    register_no = models.CharField(max_length=255)
    university_no = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True)
    roll_no = models.BigIntegerField(unique=False, null=True)
    branch = models.CharField(max_length=255, null=True)

    email = models.EmailField(unique=True, null=True)

    batch = models.BigIntegerField(unique=False, null=False)
    scheme_id = models.BigIntegerField(unique=False, null=False)
    joined_semester = models.BigIntegerField(null=False)

    photo = models.ImageField(upload_to='images/', null=True, default='images/user_default_image.png')

    def __str__(self):
        name = self.first_name + " " + self.last_name
        return name


class parents(models.Model):
    student_id = models.BigIntegerField(null=False)
    fathers_name = models.CharField(max_length=256, null=True)
    fathers_occupation = models.CharField(max_length=256, null=True)
    mothers_name = models.CharField(max_length=256, null=True)
    mothers_occupation = models.CharField(max_length=256, null=True)
    fathers_address = models.CharField(max_length=256, null=True)
    mothers_address = models.CharField(max_length=256, null=True)
    official_address = models.CharField(max_length=256, null=True)
    fathers_email_id = models.EmailField(null=True)
    mothers_email_id = models.EmailField(null=True)
    fathers_number = models.BigIntegerField(null=True)
    mothers_number = models.BigIntegerField(null=True)






