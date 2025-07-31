from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Quote

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'submitted_at', 'status')
    search_fields = ('full_name', 'email', 'phone_number')
    list_filter = ('status', 'property_type')

    
admin.site.register(CustomUser, CustomUserAdmin)
