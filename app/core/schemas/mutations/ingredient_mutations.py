from typing import Optional

import strawberry
import strawberry_django
from strawberry.types import Info
from strawberry_django.permissions import IsAuthenticated

from core.models import Ingredient
from core.schemas.types.types import IngredientType


@strawberry.type
class IngredientMutations:
    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    def create_ingredient(self, info: Info, name: str) -> IngredientType:
        user = info.context.request.user
        ingredient = Ingredient.objects.create(name=name, user=user)
        return IngredientType(id=ingredient.id, name=ingredient.name, user=user)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    def update_ingredient(self, info: Info, ingredient_id: strawberry.ID, name: Optional[str] = None) -> IngredientType:
        user = info.context.request.user
        ingredient = Ingredient.objects.get(pk=ingredient_id, user=user)
        if name:
            ingredient.name = name
            ingredient.save()
        return IngredientType(id=ingredient.id, name=ingredient.name, user=user)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    def delete_ingredient(self, info: Info, ingredient_id: strawberry.ID) -> str:
        user = info.context.request.user
        tag = Ingredient.objects.get(pk=ingredient_id, user=user)
        tag.delete()
        return f"Deleted ingredient {ingredient_id}"
