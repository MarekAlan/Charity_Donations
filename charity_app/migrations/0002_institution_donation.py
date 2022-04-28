# Generated by Django 4.0.4 on 2022-04-28 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('charity_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('Fundacja', 'Fundacja'), ('Organizacja Pozarządowa', 'Organizacja Pozarządowa'), ('Zbiórka Lokalna', 'Zbiórka Lokalna')], default='Fundacja', max_length=64)),
                ('categories', models.ManyToManyField(to='charity_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField()),
                ('address', models.CharField(max_length=64)),
                ('phone_number', models.CharField(max_length=16)),
                ('city', models.CharField(max_length=32)),
                ('zip_code', models.CharField(max_length=10)),
                ('pick_up_date', models.DateField()),
                ('pick_up_time', models.TimeField()),
                ('pick_up_comment', models.TextField()),
                ('categories', models.ManyToManyField(to='charity_app.category')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charity_app.institution')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]