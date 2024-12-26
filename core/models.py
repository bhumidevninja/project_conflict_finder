from .base import BaseModel
from django.db import models
from user.models import CustomUser


class Projects(BaseModel):
    AI = 'AI'
    WEB = 'Web Development'
    MOBILE = 'Mobile Development'

    CATEGORY_CHOICES = [
        (AI, 'AI'),
        (WEB, 'Web Development'),
        (MOBILE, 'Mobile Development'),
    ]
    title = models.CharField(max_length=200)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    keywords = models.CharField(max_length=255)

    def __str__(self):
        return self.title