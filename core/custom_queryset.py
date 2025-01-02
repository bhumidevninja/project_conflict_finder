from django.db import models

class ProjectQuerySet(models.QuerySet):
    def total_projects(self):
        return self.count()

    def approved(self):
        return self.filter(status="Approved").count()

    def rejected(self):
        return self.filter(status="Rejected").count()

    def pending(self):
        return self.filter(status="Pending").count()