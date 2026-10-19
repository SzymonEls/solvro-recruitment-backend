from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CocktailIngredientViewSet, CocktailViewSet, IngredientViewSet, RegisterView

router = DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('cocktails', CocktailViewSet)
router.register('cocktail-ingredients', CocktailIngredientViewSet)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
] + router.urls
