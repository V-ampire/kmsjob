# Generated by Django 3.2.3 on 2021-06-01 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0007_auto_20210601_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='addvacancymessage',
            name='saved_vacancy',
            field=models.BooleanField(default=False, verbose_name='Вакансия сохранена'),
        ),
    ]
