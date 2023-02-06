from django.contrib import admin

from .models import User, Category

admin.site.register(Category)
admin.site.register(User)
