# Generated by Django 3.2.8 on 2021-10-15 08:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=30)),
                ('token', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=30)),
                ('machine', models.CharField(max_length=30)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('anomaly_score', models.DecimalField(decimal_places=5, max_digits=7)),
                ('finished', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.DecimalField(decimal_places=1, max_digits=3)),
                ('humidity', models.DecimalField(decimal_places=1, max_digits=3)),
                ('volume', models.DecimalField(decimal_places=1, max_digits=4)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.part')),
            ],
        ),
    ]