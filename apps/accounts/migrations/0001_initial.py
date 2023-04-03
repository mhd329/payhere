# Generated by Django 3.2.13 on 2023-04-03 23:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_email', models.EmailField(error_messages={'unique': '이미 존재하는 이메일입니다.'}, help_text='이메일을 입력해주세요.', max_length=100, unique=True, validators=[django.core.validators.EmailValidator()], verbose_name='이메일 아이디')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='가입일')),
                ('is_admin', models.BooleanField(default=False, verbose_name='관리자 여부')),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
