# Generated by Django 5.0.2 on 2024-12-28 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0006_alter_customuser_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='location',
            field=models.CharField(blank=True, default='Not Entered yet', max_length=30),
        ),
    ]
