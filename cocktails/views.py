from rest_framework import viewsets

from .models import Ingredient, CocktailIngredient, Cocktail
from .serializers import IngredientSerializer, CocktailIngredientSerializer, CocktailSerializer
from .filters import CocktailFilter, IngredientFilter


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    ordering_fields = '__all__'

class CocktailViewSet(viewsets.ModelViewSet):
    queryset = Cocktail.objects.prefetch_related('cocktail_ingredients__ingredient')
    serializer_class = CocktailSerializer
    filterset_class = CocktailFilter
    ordering_fields = '__all__'

class CocktailIngredientViewSet(viewsets.ModelViewSet):
    queryset = CocktailIngredient.objects.select_related('ingredient', 'cocktail')
    serializer_class = CocktailIngredientSerializer
    ordering_fields = '__all__'