# Generated by Django 4.2.7 on 2023-11-17 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swapmarket', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='item_tags', to='swapmarket.category'),
        ),
    ]