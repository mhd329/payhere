# Generated by Django 3.2.13 on 2023-04-06 06:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='최초로 등록된 시간')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='마지막으로 수정된 시간')),
                ('consumption_type', models.CharField(choices=[('카드', '카드'), ('현금', '현금')], default='카드', max_length=2, verbose_name='소비유형')),
                ('breakdown', models.IntegerField(default=0, verbose_name='액수')),
                ('main_category', models.CharField(choices=[('의류비', '의류비'), ('식비', '식비'), ('주거비', '주거비'), ('기타', '기타')], default='기타', max_length=8, verbose_name='대분류')),
                ('sub_category', models.CharField(blank=True, max_length=30, null=True, verbose_name='소분류')),
                ('memo', models.CharField(blank=True, max_length=50, null=True, verbose_name='메모')),
            ],
            options={
                'db_table': 'History',
            },
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='최초로 등록된 시간')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='마지막으로 수정된 시간')),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('balance', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'UserAccount',
            },
        ),
    ]
