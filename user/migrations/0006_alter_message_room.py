# Generated by Django 4.2.7 on 2023-11-19 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_message_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='room',
            field=models.ForeignKey(max_length=1000000, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.room'),
        ),
    ]