# Generated by Django 2.1.3 on 2021-05-22 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeployStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='名称')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='描述')),
                ('change_date', models.DateTimeField(auto_now=True)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('memo', models.CharField(blank=True, max_length=1024, verbose_name='备注')),
            ],
            options={
                'ordering': ('-change_date',),
                'abstract': False,
            },
        ),
    ]
