# Generated by Django 4.2.7 on 2023-11-09 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_customuser_displayname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='displayname',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]