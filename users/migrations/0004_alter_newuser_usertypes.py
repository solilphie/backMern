# Generated by Django 4.0.4 on 2022-04-29 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_newuser_usertypes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='usertypes',
            field=models.CharField(choices=[('employer', 'EMPLOYER'), ('employee', 'EMPLOYEE')], max_length=300),
        ),
    ]
