import django_filters

from .models import Ingredient, Cocktail

class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ['name', 'is_alcoholic']

class CocktailFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    category = django_filters.CharFilter(lookup_expr='iexact')
    ingredient = django_filters.ModelChoiceFilter(field_name='ingredients', queryset=Ingredient.objects.all())
    ingredient_name = django_filters.CharFilter(field_name='ingredients__name', lookup_expr='icontains', distinct=True)
    is_alcoholic = django_filters.BooleanFilter(method='filter_is_alcoholic')

    class Meta:
        model = Cocktail
        fields = ['name', 'category', 'ingredient', 'ingredient_name', 'is_alcoholic']

    def filter_is_alcoholic(self, queryset, name, value):
        if value:
            return queryset.filter(ingredients__is_alcoholic=True).distinct()
        return queryset.exclude(ingredients__is_alcoholic=True)
