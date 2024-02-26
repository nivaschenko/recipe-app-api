from typing import Optional

import strawberry
import strawberry_django
from strawberry.types import Info
from strawberry_django.permissions import IsAuthenticated

from core.models import Tag
from core.schemas.types.types import TagType


@strawberry.type
class TagMutations:
    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    def create_tag(self, info: Info, name: str) -> TagType:
        user = info.context.request.user
        tag = Tag.objects.create(name=name, user=user)
        return TagType(id=tag.id, name=tag.name, user=user)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    def update_tag(self, info: Info, tag_id: strawberry.ID, name: Optional[str] = None) -> TagType:
        user = info.context.request.user
        tag = Tag.objects.get(pk=tag_id, user=user)
        if name:
            tag.name = name
            tag.save()
        return TagType(id=tag.id, name=tag.name, user=user)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    def delete_tag(self, info: Info, tag_id: strawberry.ID) -> str:
        user = info.context.request.user
        tag = Tag.objects.get(pk=tag_id, user=user)
        tag.delete()
        return f"Deleted tag {tag_id}"
