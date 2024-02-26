import strawberry
import strawberry_django
from strawberry_django import field as django_field

from core.schemas.mutations.mutations import Mutation
from core.schemas.types.types import RecipeType, UserType, TagType, IngredientType, UserMe


@strawberry.type
class Query:
    me: UserMe = strawberry_django.auth.current_user()

    recipe: RecipeType = django_field()

    all_recipes: list[RecipeType] = django_field()

    all_users: list[UserType] = django_field()

    all_tags: list[TagType] = django_field()

    all_ingredients: list[IngredientType] = django_field()


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
