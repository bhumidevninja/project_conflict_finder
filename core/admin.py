from django.contrib import admin
from .models import Projects,ProjectComment


admin.site.register(Projects)

@admin.register(ProjectComment)
class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ('project', 'comment', 'created_at', 'updated_at')