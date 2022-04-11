from django.contrib import admin
from .forms import UserCreationForm
from .models import IntegratedProfile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
# admin.site.register(IntegratedProfile)


# admin.site.register()


class UserAdmin(UserAdmin):
    add_form = UserCreationForm

    # define fields to be used in displaying the User model.

    list_display = ('phone_number', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('phone_number',)}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number',),
        }),
    )
    ordering = ('phone_number',)

    filter_horizontal = ()


admin.site.register(IntegratedProfile, UserAdmin)
