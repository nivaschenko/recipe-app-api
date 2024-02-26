from typing import Optional

import strawberry
import strawberry_django
from django.core.exceptions import ObjectDoesNotExist
from strawberry.file_uploads import Upload
from strawberry.types import Info
from strawberry_django.permissions import IsAuthenticated

from core.models import Recipe
from core.schemas.types.types import RecipeType, UserType


@strawberry.type
class RecipeMutations:
    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    def create_recipe(self,
                      info: Info,
                      title: str,
                      description: Optional[str],
                      time_minutes: int,
                      price: float,
                      link: Optional[str]) -> RecipeType:
        user = info.context.request.user
        recipe = Recipe.objects.create(
            title=title,
            description=description,
            time_minutes=time_minutes,
            price=price,
            link=link,
            user=user
        )
        return RecipeType(
            id=str(recipe.id),
            title=recipe.title,
            description=recipe.description,
            time_minutes=str(recipe.time_minutes),
            price=str(recipe.price),
            link=recipe.link,
            user=user,
            tags=[],
            ingredients=[]
        )

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    def update_recipe(self, info: Info, id: strawberry.ID, title: Optional[str] = None,
                      description: Optional[str] = None, time_minutes: Optional[int] = None,
                      price: Optional[float] = None, link: Optional[str] = None) -> RecipeType:
        user = info.context.request.user
        recipe = Recipe.objects.get(pk=id, user=user)

        if title is not None:
            recipe.title = title
        if description is not None:
            recipe.description = description
        if time_minutes is not None:
            recipe.time_minutes = time_minutes
        if price is not None:
            recipe.price = price
        if link is not None:
            recipe.link = link

        recipe.save()

        return RecipeType(
            id=str(recipe.id),
            title=recipe.title,
            description=recipe.description,
            time_minutes=str(recipe.time_minutes),
            price=str(recipe.price),
            link=recipe.link,
            user=user,
            tags=[],
            ingredients=[]
        )


    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    def delete_recipe(self, info: Info, id: strawberry.ID) -> str:
        user = info.context.request.user
        recipe = Recipe.objects.get(pk=id, user=user)
        recipe.delete()
        return f"Recipe {id} deleted"

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    def read_file(self, file: Upload, id: strawberry.ID) -> str:
        return file.read().decode("utf-8")

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    def upload_recipe_image(self, info: Info, recipe_id: strawberry.ID, image: Upload) -> str:
        user = info.context.request.user
        try:
            recipe = Recipe.objects.get(pk=recipe_id, user=user)
            recipe.image = image
            recipe.save()
            return f"Image for recipe {recipe_id} uploaded successfully."
        except ObjectDoesNotExist:
            return "Recipe not found."

