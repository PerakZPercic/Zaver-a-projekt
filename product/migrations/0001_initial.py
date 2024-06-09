# Generated by Django 5.0.4 on 2024-04-24 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unknown product', max_length=128)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
    ]
