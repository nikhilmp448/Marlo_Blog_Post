# Generated by Django 4.2.6 on 2023-10-27 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_rename_likes_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfeedback',
            name='aprooval',
            field=models.BooleanField(default=False),
        ),
    ]