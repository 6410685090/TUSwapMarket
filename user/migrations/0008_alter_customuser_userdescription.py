# Generated by Django 4.2.7 on 2023-11-26 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_message_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='userdescription',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]