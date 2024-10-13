from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):

    class Categories(models.TextChoices):
        WORK = ("WORK", "Work")
        PERSONAL = ("PERSONAL", "Personal")
        HEALTH = ("HEALTH", "Health")

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Owner")
    category = models.CharField(
        max_length=50, choices=Categories.choices, verbose_name="Category"
    )
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    date = models.DateField(verbose_name="Date")
    time = models.TimeField(verbose_name="Time")
    is_deleted = models.BooleanField(default=False, verbose_name="Is Deleted")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"Event: {self.pk}"

    class Meta:
        ordering = ["-date"]
        db_table = "events"
