from email.policy import default
from django.db import models


# Create your models here.
class profile(models.Model):
    Faculty_unique_id = models.CharField(max_length=255)
    Profile_photo = models.ImageField(upload_to='images/', null=True, default='images/user_default_image.png')
    First_name = models.CharField(max_length=255, null=False)
    Last_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        name = self.First_name + " " + self.Last_name
        return name


class st_feedback(models.Model):
    student_id = models.BigIntegerField()
    rating = models.CharField(max_length=255, null=True)
    revaluation = models.CharField(max_length=255, null=True)
    expected = models.CharField(max_length=255, null=True)
    revaluation_subject = models.CharField(max_length=255, null=True)
    semester = models.BigIntegerField(null=True)


class ktu_notification(models.Model):
    content = models.CharField(max_length=255, null=True)
