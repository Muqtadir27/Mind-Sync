from django.db import models

# models.py
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    studentid = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Add this

    def __str__(self):
        return self.name
