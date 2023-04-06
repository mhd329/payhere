from django.contrib import admin
from .models import UserAccount, History

# Register your models here.
admin.site.register([UserAccount, History])
