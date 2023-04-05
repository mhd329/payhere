# Generated by Django 3.2.13 on 2023-04-05 11:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accountbook', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='todayhistory',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountbook.useraccount', verbose_name='계좌'),
        ),
        migrations.AddField(
            model_name='todayhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accounttotalhistory',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountbook.useraccount', verbose_name='계좌'),
        ),
        migrations.AddField(
            model_name='accounttotalhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
