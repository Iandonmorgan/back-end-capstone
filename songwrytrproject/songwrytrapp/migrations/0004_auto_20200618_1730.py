# Generated by Django 3.0.7 on 2020-06-18 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('songwrytrapp', '0003_auto_20200616_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='recording',
            name='composition',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='songwrytrapp.Composition'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recording',
            name='image_url',
            field=models.CharField(default='http://noimage.com/image.jpg', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recording',
            name='ownership_split',
            field=models.CharField(default='50% Menna, 50% Ryan', max_length=255),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CompositionRecording',
        ),
    ]
