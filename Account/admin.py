from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Q
from rest_framework.authtoken.models import TokenProxy

from Account.models import User, AdminUser


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ['email', 'first_name', 'last_name', 'role']
    list_filter = ['is_superuser', 'role', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ("phone_number", "role", "first_name", "last_name")}),
        ('Address', {'fields': ("city", "zip", "state", "address")}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff',)}),
        ('Time Stamps', {'fields': ("date_joined", "last_login",)})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',
                       "phone_number",
                       "role",
                       "first_name",
                       "last_name",
                       'password1',
                       'password2',
                       "city",
                       "zip",
                       "state",
                       "address"
                       )}
         ),
    )

    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()

    def get_queryset(self, request):
        return self.model.objects.filter(Q(role=1) | Q(role=2) | Q(is_superuser=False) | Q(is_staff=False))


admin.site.register(User, UserAdmin)


class Admin(UserAdmin):
    model = AdminUser
    list_display = ['email', 'first_name', 'last_name', 'role', "is_staff", "is_superuser"]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ("phone_number", "role", "first_name", "last_name")}),
        ('Address', {'fields': ("city", "zip", "state", "address")}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'groups', 'user_permissions')}),
        ('Time Stamps', {'fields': ("date_joined", "last_login",)}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',
                       "phone_number",
                       "role",
                       "first_name",
                       "last_name",
                       'role',
                       'password1',
                       'password2',
                       'is_superuser',
                       'is_staff',
                       'groups',
                       'user_permissions'

                       )}
         ),
    )

    def get_queryset(self, request):
        return self.model.objects.get_admin_staff_users()


admin.site.register(AdminUser, Admin)

admin.site.unregister(TokenProxy)
