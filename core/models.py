from .base import BaseModel
from django.db import models
from user.models import CustomUser


class Projects(BaseModel):
   
    STATUS = [
        ('Pending', 'Pending'),
         ('Approved', 'Approved'),
          ('Rejected', 'Rejected'),
    ]
    title = models.CharField(max_length=200)
    frontend_tech = models.CharField(max_length=255)
    backend_tech = models.CharField(max_length=255)
    desc = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=255,choices=STATUS,default='Pending')
    keywords = models.CharField(max_length=255)

    def __str__(self):
        return self.title