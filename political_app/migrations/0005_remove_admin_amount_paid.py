# Generated by Django 4.2.13 on 2024-06-26 05:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("political_app", "0004_rename_task_status_task_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="admin",
            name="amount_paid",
        ),
    ]