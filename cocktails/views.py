from rest_framework import viewsets

from .models import Ingredient, CocktailIngredient, Cocktail
from .serializers import IngredientSerializer, CocktailIngredientSerializer, CocktailSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class CocktailViewSet(viewsets.ModelViewSet):
    queryset = Cocktail.objects.prefetch_related('cocktail_ingredients__ingredient')
    serializer_class = CocktailSerializer

class CocktailIngredientViewSet(viewsets.ModelViewSet):
    queryset = CocktailIngredient.objects.select_related('ingredient', 'cocktail')
    serializer_class = CocktailIngredientSerializer