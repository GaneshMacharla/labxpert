# Generated by Django 4.2.11 on 2024-08-14 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dailyquest', '0002_responses_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='responses',
            name='submitted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]