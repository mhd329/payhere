# Generated by Django 3.2.13 on 2023-04-03 23:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TodayHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breakdown', models.IntegerField(default=0, verbose_name='액수')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록된 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='마지막으로 수정된 시간')),
                ('main_category', models.CharField(choices=[('clothing', '의류비'), ('food', '식비'), ('shelter', '주거비'), ('general', '기타')], default='general', max_length=8, verbose_name='대분류')),
                ('sub_category', models.CharField(blank=True, max_length=30, null=True, verbose_name='소분류')),
                ('memo', models.CharField(blank=True, max_length=50, null=True, verbose_name='메모')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountbook.useraccount', verbose_name='계좌')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AccountTotalHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breakdown', models.IntegerField(default=0, verbose_name='액수')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록된 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='마지막으로 수정된 시간')),
                ('main_category', models.CharField(choices=[('clothing', '의류비'), ('food', '식비'), ('shelter', '주거비'), ('general', '기타')], default='general', max_length=8, verbose_name='대분류')),
                ('sub_category', models.CharField(blank=True, max_length=30, null=True, verbose_name='소분류')),
                ('memo', models.CharField(blank=True, max_length=50, null=True, verbose_name='메모')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountbook.useraccount', verbose_name='계좌')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
