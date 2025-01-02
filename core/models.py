from .base import BaseModel
from django.db import models
from django.core.exceptions import ValidationError
from user.models import CustomUser
from django.utils.timezone import now
from core.utils.conflict_analyzer import get_similarities
from .manager import ProjectManager


class Projects(BaseModel):

    STATUS = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]
    title = models.CharField(max_length=200)
    frontend_tech = models.CharField(max_length=255)
    backend_tech = models.CharField(max_length=255)
    desc = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS, default="Pending")
    keywords = models.CharField(max_length=255)

    objects = ProjectManager()

    def clean(self):
        # Validate status
        valid_statuses = [status[0] for status in self.STATUS]
        if self.status not in valid_statuses:
            raise ValidationError(
                f"Invalid status: '{self.status}'. Valid choices are: {valid_statuses}"
            )

        # Validate title uniqueness
        if Projects.objects.filter(title=self.title).exclude(id=self.id).exists():
            raise ValidationError(
                f"A project with the title '{self.title}' already exists."
            )

        # Validate description similarity
        existing_descs = (
            Projects.objects.filter(created_at__year=now().year)
            .exclude(id=self.id)
            .values_list("desc", flat=True)
        )
        if existing_descs:
            similar_descs = get_similarities(self.desc, list(existing_descs))
            if similar_descs:
                raise ValidationError(
                    "The description is too similar to existing projects."
                )

    def save(self, *args, **kwargs):
        # Call the clean method before saving the instance
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectComment(BaseModel):
    project = models.ForeignKey(
        "Projects", on_delete=models.CASCADE, related_name="comments"
    )
    comment = models.TextField()

    def __str__(self):
        return f"Comment on {self.project.title}"
