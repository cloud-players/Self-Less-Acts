# Generated by Django 2.1.7 on 2019-03-08 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('username', models.CharField(max_length=400, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=42)),
            ],
        ),
    ]
