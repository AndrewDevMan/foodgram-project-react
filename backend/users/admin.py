from django.contrib import admin

from users.models import User


@admin.register(User)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["email", "username"]
    list_display = ["email", "username"]
