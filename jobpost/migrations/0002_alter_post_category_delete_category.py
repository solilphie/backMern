# Generated by Django 4.0.4 on 2022-05-20 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobpost', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(max_length=250),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
