import strawberry
import strawberry_django

from license_management.models import (
    License,
    LicenseAssignment,
)
from .types import (
    LicenseType,
    LicenseAssignmentType,
)

@strawberry.type
class LicenseQuery:
    @strawberry.field
    def license(self, info, id: int) -> LicenseType:
        return License.objects.get(pk=id)
    license_list: list[LicenseType] = strawberry_django.field()

@strawberry.type
class LicenseAssignmentQuery:
    @strawberry.field
    def License_assignment(self, info, id: int) -> LicenseAssignmentType:
        return FirmwareAssignment.objects.get(pk=id)
    license_assignment_list: list[LicenseAssignmentType] = strawberry_django.field()