# Generated by Django 4.2.7 on 2023-11-26 14:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemname', models.CharField(blank=True, default='', max_length=64, null=True)),
                ('nItem', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99)])),
                ('price', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999999)])),
                ('itemdescription', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('itempicture', models.ImageField(upload_to='item_pictures/')),
                ('payment', models.CharField(blank=True, choices=[('coin', 'Coin'), ('other', 'Other')], max_length=64, null=True)),
                ('buyers', models.ManyToManyField(blank=True, related_name='items_bought', to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(blank=True, to='swapmarket.category')),
                ('itemtag', models.ManyToManyField(blank=True, related_name='item_tags', to='swapmarket.category')),
                ('seller', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='items_for_sale', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Coins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999999)])),
                ('is_confirmed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('confirmed_at', models.DateTimeField(blank=True, null=True)),
                ('nItem', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99)])),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coins', to='swapmarket.item')),
                ('receiver', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='received_coins', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sent_coins', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
