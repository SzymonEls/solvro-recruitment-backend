import django_filters
from django import forms
from .models import Ingredient, Cocktail
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter

class StrictBooleanField(forms.Field):
    def to_python(self, value):
        if value in (None, ''):
            return None
        value = str(value).lower()
        if value in ('true', '1'):
            return True
        if value in ('false', '0'):
            return False
        raise forms.ValidationError('Allowed values: true, false.')


class StrictBooleanFilter(django_filters.BooleanFilter):
    field_class = StrictBooleanField

class StrictOrderingFilter(OrderingFilter):
    def remove_invalid_fields(self, queryset, fields, view, request):
        valid_fields = super().remove_invalid_fields(queryset, fields, view, request)
        invalid_fields = []
        for field in fields:
            if field not in valid_fields:
                invalid_fields.append(field)
        if invalid_fields:
            raise ValidationError({self.ordering_param: [f'Invalid ordering field(s): {", ".join(invalid_fields)}.']})
        return valid_fields

class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    is_alcoholic = StrictBooleanFilter()

    class Meta:
        model = Ingredient
        fields = ['name', 'is_alcoholic']

class CocktailFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    category = django_filters.CharFilter(lookup_expr='iexact')
    ingredient = django_filters.ModelChoiceFilter(field_name='ingredients', queryset=Ingredient.objects.all())
    ingredient_name = django_filters.CharFilter(field_name='ingredients__name', lookup_expr='icontains', distinct=True)
    is_alcoholic = StrictBooleanFilter(method='filter_is_alcoholic')

    class Meta:
        model = Cocktail
        fields = ['name', 'category', 'ingredient', 'ingredient_name', 'is_alcoholic', 'author']

    def filter_is_alcoholic(self, queryset, name, value):
        if value:
            return queryset.filter(ingredients__is_alcoholic=True).distinct()
        return queryset.exclude(ingredients__is_alcoholic=True)
