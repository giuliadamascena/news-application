from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Publisher, Article, Newsletter


# Custom User admin to include 'role' in list display and filters
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Subscriptions', {
            'fields': ('role', 'subscriptions_to_journalists', 'subscriptions_to_publishers')
        }),
    )
    filter_horizontal = ('subscriptions_to_journalists', 'subscriptions_to_publishers')


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('editors', 'journalists')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'approved', 'created_at')
    list_filter = ('approved', 'publisher')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'journalist', 'created_at')
    search_fields = ('title', 'content')


# Register the customized User admin
admin.site.register(User, UserAdmin)
