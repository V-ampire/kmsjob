# Generated by Django 2.1.5 on 2019-06-05 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_auto_20190525_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='addvacancymessage',
            name='save_vacancy',
            field=models.BooleanField(default=False, verbose_name='Сохранить вакансию'),
        ),
    ]