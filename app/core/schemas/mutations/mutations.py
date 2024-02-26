import strawberry
from core.schemas.mutations.auth_mutations import AuthMutations
from core.schemas.mutations.ingredient_mutations import IngredientMutations
from core.schemas.mutations.recipe_mutations import RecipeMutations
from core.schemas.mutations.tag_mutaions import TagMutations


@strawberry.type
class Mutation():
    @strawberry.field(name='tagMutations')
    def tags(self) -> TagMutations:
        return TagMutations()

    @strawberry.field(name='ingredientMutations')
    def ingredients(self) -> IngredientMutations:
        return IngredientMutations()

    @strawberry.field(name='recipeMutations')
    def recipe(self) -> RecipeMutations:
        return RecipeMutations()

    @strawberry.field(name='authMutations')
    def auth(self) -> AuthMutations:
        return AuthMutations()
