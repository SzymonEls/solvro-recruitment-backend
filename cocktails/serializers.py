from rest_framework import serializers

from .models import Ingredient, CocktailIngredient, Cocktail

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import PermissionDenied


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class CocktailIngredientSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)
    cocktail_name = serializers.CharField(source='cocktail.name', read_only=True)

    class Meta:
        model = CocktailIngredient
        fields = ['id', 'cocktail', 'ingredient', 'ingredient_name', 'cocktail_name', 'amount', 'unit']

    def validate_cocktail(self, cocktail):
        user = self.context['request'].user
        if not user.is_staff and cocktail.author != user:
            raise PermissionDenied('You can only modify ingredients of your own cocktails.')
        return cocktail


class CocktailSerializer(serializers.ModelSerializer):
    ingredients = CocktailIngredientSerializer(many=True, read_only=True, source='cocktail_ingredients')
    author = serializers.StringRelatedField()

    class Meta:
        model = Cocktail
        fields = ['id', 'name', 'category', 'instruction', 'ingredients', 'author']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)