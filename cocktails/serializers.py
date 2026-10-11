from rest_framework import serializers

from .models import Ingredient, CocktailIngredient, Cocktail


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


class CocktailSerializer(serializers.ModelSerializer):
    ingredients = CocktailIngredientSerializer(many=True, read_only=True, source='cocktail_ingredients')

    class Meta:
        model = Cocktail
        fields = ['id', 'name', 'category', 'instruction', 'ingredients']