# Generated by Django 5.0.4 on 2024-04-17 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_foruminvite_rename_banmessage_forumuser_ban_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumuser',
            name='invited_by',
            field=models.IntegerField(default=0),
        ),
    ]
