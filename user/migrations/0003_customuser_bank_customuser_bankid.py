# Generated by Django 4.2.7 on 2023-12-02 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_message_room_alter_customuser_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bank',
            field=models.CharField(default='-', max_length=64),
        ),
        migrations.AddField(
            model_name='customuser',
            name='bankid',
            field=models.CharField(default='-', max_length=64),
        ),
    ]