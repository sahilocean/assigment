from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    contact_no = models.CharField(max_length=255,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table="tbl_users"
        ordering= ["-created_on"]

class Contact(models.Model):
    name=models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    description = models.TextField()
    contact_no = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "tbl_contact"
        ordering = ["-created_on"]
