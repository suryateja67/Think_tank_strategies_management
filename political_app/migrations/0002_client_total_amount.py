# Generated by Django 4.2.13 on 2024-06-25 06:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("political_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="total_amount",
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
