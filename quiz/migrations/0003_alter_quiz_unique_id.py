# Generated by Django 4.2.11 on 2024-07-09 01:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_alter_answer_question_alter_choice_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
