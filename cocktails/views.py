from .models import Ingredient, CocktailIngredient, Cocktail
from .serializers import IngredientSerializer, CocktailIngredientSerializer, CocktailSerializer
from .filters import CocktailFilter, IngredientFilter

from django.db.models import ProtectedError
from rest_framework import status, viewsets
from rest_framework.response import Response

from rest_framework import generics, permissions

from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import RegisterSerializer


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
    queryset = Cocktail.objects.select_related('author').prefetch_related('cocktail_ingredients__ingredient')
    serializer_class = CocktailSerializer
    filterset_class = CocktailFilter
    ordering_fields = '__all__'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CocktailIngredientViewSet(viewsets.ModelViewSet):
    queryset = CocktailIngredient.objects.select_related('ingredient', 'cocktail')
    serializer_class = CocktailIngredientSerializer
    ordering_fields = '__all__'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrReadOnly]

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]