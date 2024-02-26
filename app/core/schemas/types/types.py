import strawberry_django
from strawberry import auto
from typing import List, Optional

from strawberry_django import field, filters
from django.contrib.auth import get_user_model
from strawberry_django.permissions import IsAuthenticated

from core.models import Recipe, User, Tag, Ingredient


class BaseType:

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        user = info.context.request.user
        return queryset.filter(user=user)


@strawberry_django.type(get_user_model())
class UserMe:
    name: str
    email: str


@strawberry_django.input(get_user_model())
class UserInput:
    name: auto
    password: auto


@strawberry_django.type(model=User, pagination=True)
class UserType:
    email: str = field(extensions=[IsAuthenticated()])
    name: str = field(extensions=[IsAuthenticated()])


@strawberry_django.type(model=Tag, pagination=True)
class TagType(BaseType):
    id: str = field(extensions=[IsAuthenticated()])
    name: str = field(extensions=[IsAuthenticated()])
    user: UserType


@strawberry_django.type(model=Ingredient, pagination=True)
class IngredientType(BaseType):
    id: str = field(extensions=[IsAuthenticated()])
    name: str = field(extensions=[IsAuthenticated()])
    user: UserType = field(extensions=[IsAuthenticated()])


@strawberry_django.filter(model=Recipe)
class RecipeFilter:
    tags: auto
    ingredients: auto


@strawberry_django.type(
    model=Recipe,
    pagination=True,
    filters=RecipeFilter
)
class RecipeType(BaseType):
    id: str = field(extensions=[IsAuthenticated()])
    title: str = field(extensions=[IsAuthenticated()])
    description: Optional[str] = field(extensions=[IsAuthenticated()])
    time_minutes: str = field(extensions=[IsAuthenticated()])
    price: str = field(extensions=[IsAuthenticated()])
    link: Optional[str] = field(extensions=[IsAuthenticated()])
    user: UserType = field(extensions=[IsAuthenticated()])
    tags: List[TagType] = field(extensions=[IsAuthenticated()])
    ingredients: List[IngredientType] = field(extensions=[IsAuthenticated()])
    image: str

    @strawberry_django.field(extensions=[IsAuthenticated()])
    def image(self, info) -> str:
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ''


def resolve_tags(recipe: RecipeType) -> List[TagType]:
    return TagType.objects.filter(recipe=recipe.id)


def resolve_ingredients(recipe: RecipeType) -> List[IngredientType]:
    return IngredientType.objects.filter(recipe=recipe.id)


RecipeType.tags = strawberry_django.field(resolver=resolve_tags)
RecipeType.ingredients = strawberry_django.field(resolver=resolve_ingredients)
