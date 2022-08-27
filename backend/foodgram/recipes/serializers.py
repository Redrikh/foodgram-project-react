from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, validators
from users.mixins import IsSubscribedMixin
from users.serializers import UserSerializer

from .models import (
    FavoriteRecipe,
    Ingredient,
    IngredientsRecipe,
    Recipe,
    ShoppingCart,
    Tag,
    TagsRecipe,
)

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиентов."""
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement',
        )


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиентов в рецепте."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id',
    )
    name = serializers.CharField(
        read_only=True,
        source='ingredient.name'
    )
    measurement = serializers.CharField(
        read_only=True,
        source='ingredient.measurement'
    )

    class Meta:
        model = IngredientsRecipe
        fields = (
            'id',
            'name',
            'measurement',
            'amount',
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""
    class Meta:
        model = Tag
        fields = '__all__'
        lookup_field = 'slug'


class CreateRecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
    )
    author = UserSerializer(read_only=True)
    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    ingredients = IngredientsRecipeSerializer(
        many=True,
        source='recipe_ingredients',
    )
    text = serializers.CharField()
    image = Base64ImageField(use_url=True)
    cooking_time = serializers.IntegerField(min_value=1, max_value=14400)

    class Meta:
        model = Recipe
        fields = ('__all__')

    def create_tags(self, recipe, tags):
        TagsRecipe.objects.bulk_create(
            [TagsRecipe(
                recipe=recipe,
                tag=Tag.objects.get(id=tag),
            ) for tag in tags]
        )

    def create_ingredients(self, recipe, ingredients):
        IngredientsRecipe.objects.bulk_create(
            [IngredientsRecipe(
                recipe=recipe,
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                amount=ingredient['amount'],
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):
        context = self.context['request']
        validated_data.pop('recipe_ingredients')
        recipe = Recipe.objects.create(
            **validated_data,
            author=self.context.get('request').user
        )
        tags = context.data['tags']
        self.create_tags(recipe, tags)
        ingredients = context.data['ingredients']
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, recipe, validated_data):
        context = self.context['request']
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get(
            'cooking_time',
            recipe.cooking_time,
        )
        recipe.image = validated_data.get('image', recipe.image)
        recipe.save()
        tags = context.data['tags']
        TagsRecipe.objects.filter(recipe=recipe).delete()
        self.create_tags(recipe, tags)
        ingredients = context.data['ingredients']
        IngredientsRecipe.objects.filter(recipe=recipe).delete()
        self.create_ingredients(recipe, ingredients)
        return recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""
    name = serializers.CharField(
        required=True,
    )
    author = UserSerializer(read_only=True)
    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    ingredients = IngredientsRecipeSerializer(
        many=True,
        source='recipe_ingredients',
    )
    text = serializers.CharField()
    image = Base64ImageField(use_url=True)
    cooking_time = serializers.IntegerField(min_value=1, max_value=14400)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'name',
            'author',
            'ingredients',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_user(self):
        return self.context.get('request').user

    def get_request(self):
        return self.context.get('request')

    def get_is_favorited(self, obj):
        request = self.get_request()
        user = self.get_user()
        if not request or request.user.is_anonymous:
            return False
        return user.favorite_recipes.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.get_request()
        user = self.get_user()
        if not request or request.user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()


class FavoritedSerializer(serializers.ModelSerializer):
    """Сериализатор избранного."""
    id = serializers.CharField(
        read_only=True,
        source='recipe.id',
    )
    cooking_time = serializers.CharField(
        read_only=True,
        source='recipe.cooking_time',
    )
    image = serializers.CharField(
        read_only=True,
        source='recipe.image',
    )
    name = serializers.CharField(
        read_only=True,
        source='recipe.name',
    )

    def validate(self, data):
        recipe = data['recipe']
        user = data['user']
        if user == recipe.author:
            raise serializers.ValidationError(
                'Нельзя добавить в избранное свой рецепт.'
            )
        if FavoriteRecipe.objects.filter(recipe=recipe, user=user).exists():
            raise serializers.ValidationError('Рецепт уже в избранном.')
        return data

    def create(self, validated_data):
        favorite = FavoriteRecipe.objects.create(**validated_data)
        favorite.save()
        return favorite

    class Meta:
        model = FavoriteRecipe
        fields = (
            'id',
            'cooking_time',
            'name',
            'image',
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор корзины покупок."""
    id = serializers.CharField(
        read_only=True,
        source='recipe.id',
    )
    cooking_time = serializers.CharField(
        read_only=True,
        source='recipe.cooking_time',
    )
    image = serializers.CharField(
        read_only=True,
        source='recipe.image',
    )
    name = serializers.CharField(
        read_only=True,
        source='recipe.name',
    )

    class Meta:
        model = ShoppingCart
        fields = (
            'id',
            'cooking_time',
            'name',
            'image',
        )


class SubscribeSerializer(serializers.ModelSerializer, IsSubscribedMixin):
    """Сериализатор подписок."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField('get_recipes_count')
    username = serializers.CharField(
        required=True,
        validators=[validators.UniqueValidator(
            queryset=User.objects.all()
        )]
    )

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'recipes',
            'recipes_count',
            'is_subscribed',
        ]

    def get_recipes_count(self, data):
        return Recipe.objects.filter(author=data).count()

    def get_recipes(self, data):
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        recipes = (
            data.recipes.all()[:int(recipes_limit)]
            if recipes_limit else data.recipes
        )
        serializer = serializers.ListSerializer(child=RecipeSerializer())
        return serializer.to_representation(recipes)
