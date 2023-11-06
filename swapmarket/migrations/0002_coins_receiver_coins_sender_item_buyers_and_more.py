# Generated by Django 4.2.7 on 2023-11-06 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('swapmarket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coins',
            name='receiver',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='received_coins', to='user.customuser'),
        ),
        migrations.AddField(
            model_name='coins',
            name='sender',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sent_coins', to='user.customuser'),
        ),
        migrations.AddField(
            model_name='item',
            name='buyers',
            field=models.ManyToManyField(blank=True, related_name='items_bought', to='user.customuser'),
        ),
        migrations.AddField(
            model_name='item',
            name='categories',
            field=models.ManyToManyField(blank=True, to='swapmarket.category'),
        ),
        migrations.AddField(
            model_name='item',
            name='seller',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='items_for_sale', to='user.customuser'),
        ),
    ]
