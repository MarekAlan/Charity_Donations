# Generated by Django 4.0.4 on 2022-05-01 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity_app', '0002_institution_donation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='pick_up_date',
            field=models.DateField(null=True),
        ),
    ]