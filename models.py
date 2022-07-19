from django.db import models


# Create your models here.
class login(models.Model):
    email = models.EmailField(unique=True, primary_key=True)
    password = models.CharField(null=False, max_length=255)

    cat = [
        ('Student', 'Student'),
        ('Admin', 'Admin')
    ]
    category = models.CharField(max_length=255, choices=cat)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        name = self.email
        return name
