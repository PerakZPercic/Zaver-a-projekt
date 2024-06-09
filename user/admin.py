from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .forms import ForumUserCreationForm, ForumUserChangeForm
from .models import ForumInvite, ForumUser


class ForumInviteFilter(admin.SimpleListFilter):
    title = "Users"
    parameter_name = "All"

    def lookups(self, request, model_admin):
        already_added_list = {}
        final_list = []

        for inv in model_admin.model.objects.all():
            user_id = inv.created_by
            if already_added_list.get(user_id) is True:
                continue

            final_list += [(user_id, inv.get_creator_name())]
            already_added_list[user_id] = True

        return final_list

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(created_by=self.value())


class ForumInviteAdmin(admin.ModelAdmin):
    model = ForumInvite

    list_filter = (ForumInviteFilter,)


class ForumUserAdmin(UserAdmin):
    add_form = ForumUserCreationForm
    form = ForumUserChangeForm
    model = ForumUser

    list_display = ("username", "id", "email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "is_active")}),
        ("Ban stuff", {"fields": ("is_banned", "banned_until", "ban_message")}),
        ("Permissions", {"fields": ("is_staff", "groups", "user_permissions")}),
        ("Invites", {"fields": ("invited_by", "created_invites", "used_invites")})
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "password1", "password2", "invite_code"
            )
        }),
    )
    search_fields = ("username",)
    ordering = ("username",)


admin.site.register(ForumInvite, ForumInviteAdmin)
admin.site.register(ForumUser, ForumUserAdmin)
