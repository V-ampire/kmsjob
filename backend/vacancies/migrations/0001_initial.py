# Generated by Django 3.2.3 on 2021-05-27 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('modified', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('name', models.CharField(max_length=255, verbose_name='Вакансия')),
                ('employer', models.CharField(blank=True, max_length=255, verbose_name='Работодатель')),
                ('source', models.URLField(blank=True, verbose_name='Ссылка на вакансию')),
                ('source_name', models.CharField(default='kmsjob', max_length=50, verbose_name='Название источника')),
                ('description', models.TextField(blank=True, verbose_name='Описание вакансии')),
                ('contacts', models.CharField(blank=True, max_length=125, verbose_name='Контакты')),
                ('status', models.CharField(choices=[('on', 'Показывать'), ('off', 'Не показывать')], default='on', max_length=3, verbose_name='Статус вакансии')),
            ],
            options={
                'ordering': ('source', '-modified'),
            },
        ),
    ]
