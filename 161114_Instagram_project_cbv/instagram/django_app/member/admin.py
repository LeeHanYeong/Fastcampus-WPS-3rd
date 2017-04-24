from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser


class MyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'fields': (
                'username',
                'password1',
                'password2',
                'last_name',
                'first_name',
            )
        }),
    )


admin.site.register(MyUser, MyUserAdmin)