from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, CocktailViewSet, CocktailIngredientViewSet

router = DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('cocktails', CocktailViewSet)
router.register('cocktail-ingredients', CocktailIngredientViewSet)

urlpatterns = router.urls