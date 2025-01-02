from django.db import models
from .custom_queryset import ProjectQuerySet

class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)

    def total_projects(self):
        return self.get_queryset().total_projects()

    def approved(self):
        return self.get_queryset().approved()

    def rejected(self):
        return self.get_queryset().rejected()

    def pending(self):
        return self.get_queryset().pending()