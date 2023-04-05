from django.contrib import admin
from .models import UserAccount, TodayHistory, AccountTotalHistory

# Register your models here.
admin.site.register([UserAccount, TodayHistory, AccountTotalHistory])