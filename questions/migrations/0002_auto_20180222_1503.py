# Generated by Django 2.0.2 on 2018-02-22 13:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='pub_time',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Answer Date'),
        ),
        migrations.AlterField(
            model_name='answercomment',
            name='pub_time',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Comment Date'),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_time',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Question Date'),
        ),
        migrations.AlterField(
            model_name='questioncomment',
            name='pub_time',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Comment Date'),
        ),
    ]