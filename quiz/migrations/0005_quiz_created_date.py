# Generated by Django 4.2.11 on 2024-07-11 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_alter_answer_question_alter_choice_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='created_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
