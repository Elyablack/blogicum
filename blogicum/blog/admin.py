from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from .models import Category, Comment, Location, Post, User

admin.site.empty_value_display = 'Не задано'
admin.site.unregister(User)
admin.site.unregister(Group)


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    @admin.display(description='Количество постов у пользователя')
    def posts_count(self, obj):
        return obj.posts.count()

    list_display = BaseUserAdmin.list_display + ('posts_count',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at',
    )
    list_filter = ('is_published',)
    search_fields = ('title', 'description')
    list_editable = ('is_published',)
    list_display_links = ('title', 'slug')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = (
        'name',
        'is_published',
        'created_at'
    )
    list_filter = ('is_published',)
    search_fields = ('name',)
    list_editable = ('is_published',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'author',
        'category',
        'pub_date',
        'is_published',
        'display_image',
    )
    list_filter = ('is_published', 'pub_date', 'category', 'location')
    search_fields = ('title', 'text')
    list_editable = ('is_published',)
    list_display_links = ('title', 'category')

    @admin.display(description='Изображение')
    def display_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="80" height="60">'
            )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'text',
        'author',
        'created_at',
    )
    list_filter = ('post', 'author',)
    search_fields = ('post', 'author')
    list_display_links = ('post', 'author')
