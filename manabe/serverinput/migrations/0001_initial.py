# Generated by Django 2.1.3 on 2021-05-22 02:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('envx', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appinput', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='名称')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='描述')),
                ('change_date', models.DateTimeField(auto_now=True)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('ip_address', models.CharField(max_length=24, verbose_name='IP地址')),
                ('salt_name', models.CharField(max_length=128, verbose_name='SaltStack minion')),
                ('port', models.CharField(max_length=100, verbose_name='端口')),
                ('app_user', models.CharField(blank=True, max_length=24, null=True, verbose_name='执行程序用户')),
                ('history_deploy', models.CharField(blank=True, max_length=512, null=True, verbose_name='已部署版本')),
                ('deploy_status', models.CharField(blank=True, max_length=128, null=True, verbose_name='发布状态(Err,Suc)')),
                ('app_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_name', to='appinput.App', verbose_name='应用名')),
                ('env_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='server_env_name', to='envx.Env', verbose_name='环境')),
                ('op_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='操作用户')),
            ],
            options={
                'ordering': ('-change_date',),
                'abstract': False,
            },
        ),
    ]
