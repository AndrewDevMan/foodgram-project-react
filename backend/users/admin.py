from django.contrib import admin

from users.models import Follow, User

admin.site.empty_value_display = "---"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка для User"""
    search_fields = ["email", "username", "id", "first_name", "last_name"]
    list_display = ["id", "email", "username"]


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Админка для Follow"""
    list_display = ["user", "author"]
