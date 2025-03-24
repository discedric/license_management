import django_filters
from django.db.models import Q
from .models import License, LicenseAssignment
from netbox.filtersets import NetBoxModelFilterSet
from dcim.models import Manufacturer, Device
from virtualization.models import VirtualMachine


class LicenseFilterSet(NetBoxModelFilterSet):
    """Filterset for Software Licenses with enhanced search capability."""

    q = django_filters.CharFilter(method="search", label="Search")

    manufacturer = django_filters.ModelChoiceFilter(
        queryset=Manufacturer.objects.all(),
        field_name="manufacturer",
        label="License Manufacturer"
    )

    volume_type = django_filters.ChoiceFilter(
        choices=License.VOLUME_TYPE_CHOICES,
        label="Volume Type"
    )

    purchase_date = django_filters.DateFromToRangeFilter(label="Purchase Date (Between)")
    expiry_date = django_filters.DateFromToRangeFilter(label="Expiry Date (Between)")

    parent_license = django_filters.ModelChoiceFilter(
        queryset=License.objects.filter(parent_license__isnull=True),
        label="Parent License"
    )

    class Meta:
        model = License
        fields = [
            "license_key",
            "product_key",
            "serial_number",
            "name",
            "manufacturer",
            "volume_type",
            "purchase_date",
            "expiry_date",
            "parent_license",
        ]

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(license_key__icontains=value) |
            Q(product_key__icontains=value) |
            Q(serial_number__icontains=value)
        ).distinct()


class LicenseAssignmentFilterSet(NetBoxModelFilterSet):
    """Filterset for License Assignments with comprehensive filtering."""
    q = django_filters.CharFilter(method="search", label="Search")

    license = django_filters.ModelChoiceFilter(
        queryset=License.objects.all(),
        label="License"
    )

    device = django_filters.ModelChoiceFilter(queryset=Device.objects.all(), label="Device")
    virtual_machine = django_filters.ModelChoiceFilter(queryset=VirtualMachine.objects.all(), label="Virtual Machine")

    manufacturer = django_filters.ModelChoiceFilter(
        field_name="license__manufacturer",
        queryset=Manufacturer.objects.all(),
        label="License Manufacturer"
    )

    device_manufacturer = django_filters.ModelChoiceFilter(
        field_name="device__device_type__manufacturer",
        queryset=Manufacturer.objects.all(),
        label="Device Manufacturer"
    )

    assigned_to = django_filters.DateFromToRangeFilter(label="Assigned Date (Between)")
    volume = django_filters.NumberFilter(label="Volume")

    class Meta:
        model = LicenseAssignment
        fields = [
            "license",
            "device",
            "virtual_machine",
            "manufacturer",
            "device_manufacturer",
            "assigned_to",
            "volume",
        ]

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(license__name__icontains=value)
            | Q(license__license_key__icontains=value)
            | Q(license__manufacturer__name__icontains=value)
            | Q(device__name__icontains=value)
            | Q(virtual_machine__name__icontains=value)
        ).distinct()
