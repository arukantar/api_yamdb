# Generated by Django 3.2 on 2023-02-02 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default=11111111, max_length=8),
            preserve_default=False,
        ),
    ]