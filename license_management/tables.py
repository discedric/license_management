from django.db.models import Sum
from django_tables2 import tables
from netbox.tables import NetBoxTable
from .models import License, LicenseAssignment


class LicenseTable(NetBoxTable):
    name = tables.Column(linkify=True)
    license_key = tables.Column(linkify=True)
    product_key = tables.Column(verbose_name="Product Key")
    manufacturer = tables.Column(
        verbose_name="License Manufacturer",
        accessor="manufacturer",
        linkify=True
    )
    parent_license = tables.Column(
        accessor="parent_license",
        verbose_name="Parent License",
        linkify=True
    )
    
    volume_type = tables.Column(verbose_name="Volume Type")

    is_parent_license = tables.Column(
        verbose_name='Parent?',
        empty_values=()
    )

    is_child_license = tables.Column(
        verbose_name='Child?',
        empty_values=()
    )

    assigned_count = tables.Column(empty_values=(), verbose_name="Assigned")

    def render_assigned_count(self, record):
        assigned = record.assignments.aggregate(total=Sum('volume'))['total'] or 0
        if record.volume_type == "UNLIMITED":
            return f"{assigned}/∞"
        elif record.volume_type == "VOLUME":
            return f"{assigned}/{record.volume_limit or '∞'}"
        return f"{assigned}/1"

    
    def render_is_parent_license(self, record):
        return "✅" if record.is_parent_license else "❌"

    def render_is_child_license(self, record):
        return "✅" if record.is_child_license else "❌"

    class Meta(NetBoxTable.Meta):
        model = License
        fields = (
            "name", "license_key", "product_key",
            "manufacturer", "parent_license",
            "is_parent_license", "is_child_license", "description",
            "assigned_count", "volume_type",
            "expiry_date", "purchase_date",
        )
        default_columns = fields
        attrs = {"class": "table table-striped table-bordered"}



class LicenseAssignmentTable(NetBoxTable):
    license = tables.Column(
        accessor="license",
        verbose_name="License",
        linkify=True
    )
    license_key = tables.Column(
        accessor="license.license_key",
        verbose_name="License Key",
        linkify=True
    )
    manufacturer = tables.Column(
        accessor="license.manufacturer",
        verbose_name="License Manufacturer",
        linkify=True
    )
    device = tables.Column(
        accessor="device",
        verbose_name="Device",
        linkify=True
    )
    device_manufacturer = tables.Column(
        accessor="device.device_type.manufacturer",
        verbose_name="Device Manufacturer",
        linkify=True
    )
    virtual_machine = tables.Column(
        accessor="virtual_machine",
        verbose_name="Virtual Machine",
        linkify=True
    )
    volume = tables.Column(verbose_name="Volume")
    assigned_to = tables.Column(verbose_name="Assigned On")
    description = tables.Column(verbose_name="Description")

    class Meta(NetBoxTable.Meta):
        model = LicenseAssignment
        fields = (
            "license", "license_key", "manufacturer",
            "device", "device_manufacturer",
            "virtual_machine", "volume",
            "assigned_to", "description"
        )
        attrs = {"class": "table table-striped table-bordered"}
