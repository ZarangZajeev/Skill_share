# Generated by Django 4.2.6 on 2024-03-07 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('pass', 'pass'), ('failed', 'failed')], default='pending', max_length=200),
        ),
    ]