# Generated by Django 3.0.7 on 2020-06-16 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('songwrytrapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='writer',
            name='pro',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='songwrytrapp.PRO'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='writer',
            name='pro_acct_num',
            field=models.IntegerField(default=123),
            preserve_default=False,
        ),
    ]