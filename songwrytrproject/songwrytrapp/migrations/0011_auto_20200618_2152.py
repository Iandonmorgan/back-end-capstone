# Generated by Django 3.0.7 on 2020-06-18 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songwrytrapp', '0010_auto_20200618_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recording',
            name='is_delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='recording',
            name='is_mastered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='recording',
            name='is_mixed',
            field=models.BooleanField(default=False),
        ),
    ]