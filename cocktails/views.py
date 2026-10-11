from .models import Ingredient, CocktailIngredient, Cocktail
from .serializers import IngredientSerializer, CocktailIngredientSerializer, CocktailSerializer
from .filters import CocktailFilter, IngredientFilter

from django.db.models import ProtectedError
from rest_framework import status, viewsets
from rest_framework.response import Response


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    ordering_fields = '__all__'

    def destroy(self, request, *args, **kwargs):
        ingredient = self.get_object()
        try:
            ingredient.delete()
        except ProtectedError:
            cocktails = ingredient.cocktails.values_list('name', flat=True)
            return Response(
                {
                    'detail': 'Ingredient is used in cocktails and cannot be deleted.',
                    'cocktails': list(cocktails),
                },
                status=status.HTTP_409_CONFLICT,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class CocktailViewSet(viewsets.ModelViewSet):
    queryset = Cocktail.objects.prefetch_related('cocktail_ingredients__ingredient')
    serializer_class = CocktailSerializer
    filterset_class = CocktailFilter
    ordering_fields = '__all__'

class CocktailIngredientViewSet(viewsets.ModelViewSet):
    queryset = CocktailIngredient.objects.select_related('ingredient', 'cocktail')
    serializer_class = CocktailIngredientSerializer
    ordering_fields = '__all__'