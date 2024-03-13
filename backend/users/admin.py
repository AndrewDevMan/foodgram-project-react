from django.contrib import admin

from users.models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ["email", "username"]
    list_display = ["email", "username"]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass
