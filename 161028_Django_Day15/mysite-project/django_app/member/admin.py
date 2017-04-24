from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from member.models import MyUser


# Django에서 기본으로 제공하는 UserCreationForm을 상속받아 사용
# UserCreationForm은 ModelForm을 상속받으므로 Meta에 model과 fields를 정의해준다
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = '__all__'


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = '__all__'


class MyUserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'id', 'date_joined', )
    list_filter = ('is_staff', )
    ordering = ('-date_joined', )
    readonly_fields = ('date_joined', )
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
                'nickname',
            )
        }),
        ('Personal Info', {
            'fields': (
                'last_name',
                'first_name',
                'phone_number',
            )
        }),
        ('Facebook Info', {
            'fields': (
                'is_facebook_user',
                'facebook_id',
                'img_profile_url',
            )
        }),
        ('Additional Info', {
            'fields': (
                'is_superuser',
                'is_staff',
                'date_joined',
            )
        })
    )
    add_fieldsets = (
        (None, {
            'fields': (
                'email',
                'password1',
                'password2',
                'last_name',
                'first_name',
                'is_staff',
            )
        }),
    )

    add_form = MyUserCreationForm
    form = MyUserChangeForm


admin.site.register(MyUser, MyUserAdmin)