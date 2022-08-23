from django.contrib import admin
from django.contrib.auth import get_user_model

from recipes.models import (
    Ingredient,
    IngredientsRecipe,
    Recipe,
    Tag,
    TagsRecipe,
    Subscribe,
)

User = get_user_model()


class IngredientsInline(admin.TabularInline):
    model = IngredientsRecipe
    extra = 1


class TagsInline(admin.TabularInline):
    model = TagsRecipe
    extra = 1


class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'first_name', 'last_name', 'email')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    empty_value_display = "-пусто-"


class FollowsAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscribing')
    list_filter = ('user', 'subscribing')
    search_fields = ('user', 'subscribing')
    empty_value_display = "-пусто-"


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_recipes_favorite')
    list_filter = ('name', 'author')
    search_fields = ('name', 'author', 'tags')
    empty_value_display = "-пусто-"
    inlines = [
        TagsInline, IngredientsInline
    ]
    readonly_fields = ['count_recipes_favorite']

    def count_recipes_favorite(self, obj):
        return obj.favorite_recipes.count()

    count_recipes_favorite.short_description = 'Популярность'


class TagsAdmin(admin.ModelAdmin):
    inlines = [
        TagsInline
    ]
    list_display = ('name', 'color')
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientsAdmin(admin.ModelAdmin):
    inlines = [
        IngredientsInline
    ]
    list_display = ('name', 'measurement')
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(User, UsersAdmin)
admin.site.register(Subscribe, FollowsAdmin)
admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Tag, TagsAdmin)
admin.site.register(Ingredient, IngredientsAdmin)
