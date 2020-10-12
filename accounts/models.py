import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    contact_no = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tbl_users"
        ordering = ["-created_on"]


class Contact(models.Model):
    STATUS = ((0, "No Mail"), (1, "To Admin"), (2, "To User"))
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    description = models.TextField()
    contact_no = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    admin_time = models.DateTimeField(null=True)
    user_time = models.DateTimeField(null=True)
    status = models.PositiveIntegerField(default=0, choices=STATUS)

    class Meta:
        db_table = "tbl_contact"
        ordering = ["-created_on"]

    def save(self, *args, **kwargs):
        self.user_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
        self.admin_time = datetime.datetime.now() + datetime.timedelta(minutes=20)
        super().save(*args, **kwargs)
