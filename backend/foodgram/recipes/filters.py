from django_filters import rest_framework as filters

from .models import Recipe, Ingredient, Tag


class IngredientFilter(filters.FilterSet):
    """Filter fo ingredients"""
    name = filters.CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    """Фильтр для рецептов."""
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    author = filters.CharFilter(lookup_expr='exact')
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='filter',
    )
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
        method='filter',
    )

    def filter(self, queryset, name, value):
        if name == 'is_in_shopping_cart' and value:
            queryset = queryset.filter(
                shopping_cart__user=self.request.user
            )
        if name == 'is_favorited' and value:
            queryset = queryset.filter(
                favorite_recipes__user=self.request.user
            )
        return queryset

    class Meta:
        model = Recipe
        fields = [
            'author',
            'tags',
            'is_in_shopping_cart',
            'is_favorited',
        ]
