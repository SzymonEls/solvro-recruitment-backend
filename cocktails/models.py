from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    is_alcoholic = models.BooleanField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Cocktail(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=200)
    instruction = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='CocktailIngredient', related_name='cocktails')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class CocktailIngredient(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE, related_name='cocktail_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT, related_name='cocktail_ingredients')
    amount = models.DecimalField(max_digits=8, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    unit = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cocktail', 'ingredient'], name='unique_ingredient_per_cocktail'),
        ]


    def __str__(self):
        return f'{self.amount} {self.unit} {self.ingredient} in {self.cocktail} cocktail'
