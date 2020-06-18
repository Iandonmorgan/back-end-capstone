# Generated by Django 3.0.7 on 2020-06-18 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songwrytrapp', '0005_auto_20200618_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recording',
            name='is_delivered',
            field=models.BooleanField(default=False, verbose_name='IS delivered'),
        ),
        migrations.AlterField(
            model_name='recording',
            name='is_mastered',
            field=models.BooleanField(default=False, verbose_name='IS mastered'),
        ),
        migrations.AlterField(
            model_name='recording',
            name='is_mixed',
            field=models.BooleanField(default=False, verbose_name='IS mixed'),
        ),
    ]