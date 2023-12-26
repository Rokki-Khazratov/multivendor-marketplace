# app name - api
from django.db import models

class DocumentationSection(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    parent_section = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


