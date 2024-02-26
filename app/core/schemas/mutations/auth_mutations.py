import strawberry
import strawberry_django

from core.schemas.types.types import UserMe, UserInput


@strawberry.type
class AuthMutations:
    login: UserMe = strawberry_django.auth.login()
    logout = strawberry_django.auth.logout()
    register: UserMe = strawberry_django.auth.register(UserInput)
