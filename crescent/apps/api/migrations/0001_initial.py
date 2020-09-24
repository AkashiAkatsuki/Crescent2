# Generated by Django 3.1.1 on 2020-09-24 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('category', models.IntegerField()),
                ('value', models.FloatField(default=0.5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'words',
            },
        ),
        migrations.CreateModel(
            name='Markov',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix1', models.IntegerField()),
                ('prefix2', models.IntegerField()),
                ('suffix', models.IntegerField()),
            ],
            options={
                'db_table': 'markovs',
                'unique_together': {('prefix1', 'prefix2', 'suffix')},
            },
        ),
    ]
