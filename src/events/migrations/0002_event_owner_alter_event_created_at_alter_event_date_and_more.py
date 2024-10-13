# Generated by Django 5.1.2 on 2024-10-13 12:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="owner",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Owner",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="event",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
        ),
        migrations.AlterField(
            model_name="event",
            name="date",
            field=models.DateField(verbose_name="Date"),
        ),
        migrations.AlterField(
            model_name="event",
            name="is_deleted",
            field=models.BooleanField(default=False, verbose_name="Is Deleted"),
        ),
        migrations.AlterField(
            model_name="event",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated At"),
        ),
    ]
