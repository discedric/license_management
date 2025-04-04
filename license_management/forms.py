from django import forms
from .models import License, LicenseAssignment
from dcim.models import Manufacturer, Device
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm
from .filtersets import LicenseAssignmentFilterSet, LicenseFilterSet
from virtualization.models import VirtualMachine, Cluster
from utilities.forms.rendering import FieldSet, TabbedGroups
from netbox.forms import NetBoxModelImportForm
from utilities.forms.fields import CSVModelChoiceField, CSVChoiceField


class LicenseFilterForm(NetBoxModelFilterSetForm):
    model = License
    filterset_class = LicenseFilterSet

    fieldsets = (
        FieldSet('q', name='Search'),
        FieldSet('manufacturer_id', 'volume_type', 'license_key', 'product_key', 'serial_number', name='License Info'),
        FieldSet('is_parent_license', 'is_child_license', 'parent_license', 'child_license', name='License Relationship'),
        FieldSet('purchase_date_after', 'purchase_date_before', 'expiry_date_after', 'expiry_date_before', name='Dates'),
    )



    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="License Manufacturer"
    )

    parent_license = DynamicModelChoiceField(
        queryset=License.objects.filter(parent_license__isnull=True),
        required=False,
        label="Parent License",
        query_params={'manufacturer_id': '$manufacturer_id'}
    )

    child_license = DynamicModelMultipleChoiceField(
        queryset=License.objects.filter(sub_licenses__isnull=False),
        required=False,
        label="Child Licenses",
        query_params={'manufacturer_id': '$manufacturer_id'}
    )

    is_parent_license = forms.NullBooleanField(
        required=False,
        label="Is Parent License",
        widget=forms.Select(choices=[('', '---------'), (True, 'Yes'), (False, 'No')])
    )

    is_child_license = forms.NullBooleanField(
        required=False,
        label="Is Child License",
        widget=forms.Select(choices=[('', '---------'), (True, 'Yes'), (False, 'No')])
    )

    volume_type = forms.ChoiceField(
        choices=[('', '---------')] + License.VOLUME_TYPE_CHOICES,
        required=False,
        label="Volume Type"
    )

    name = forms.CharField(
        required=False,
        label="Name"
    )

    license_key = forms.CharField(
        required=False,
        label="License Key"
    )

    product_key = forms.CharField(
        required=False,
        label="Product Key"
    )

    serial_number = forms.CharField(
        required=False,
        label="Serial Number"
    )

    purchase_date_after = forms.DateField(
        required=False,
        label="Purchase Date (After)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    purchase_date_before = forms.DateField(
        required=False,
        label="Purchase Date (Before)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    expiry_date_after = forms.DateField(
        required=False,
        label="Expiry Date (After)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    expiry_date_before = forms.DateField(
        required=False,
        label="Expiry Date (Before)",
        widget=forms.DateInput(attrs={'type': 'date'})
    )


class LicenseImportForm(NetBoxModelImportForm):
    manufacturer = CSVModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        label='Manufacturer',
        help_text='The license manufacturer'
    )

    parent_license = CSVModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        to_field_name='license_key',
        label='Parent License',
        help_text='Parent license key if applicable'
    )

    volume_type = CSVChoiceField(
        choices=License.VOLUME_TYPE_CHOICES,
        label='Volume Type',
        help_text='License volume type'
    )

    class Meta:
        model = License
        fields = [
            "name", "license_key", "product_key", "serial_number", "description",
            "manufacturer", "purchase_date", "expiry_date",
            "volume_type", "volume_limit", "parent_license"
        ]
        labels = {
            "name": "License Name",
            "license_key": "License Key",
            "product_key": "Product Key",
            "serial_number": "Serial Number",
            "description": "Description",
            "manufacturer": "Manufacturer",
            "purchase_date": "Purchase Date",
            "expiry_date": "Expiry Date",
            "volume_type": "Volume Type",
            "volume_limit": "Volume Limit",
            "parent_license": "Parent License",
        }
        help_texts = {
            "name": "Name of the license",
            "license_key": "Unique license key",
            "product_key": "Product key for activation",
            "serial_number": "Serial number of the license",
            "description": "Additional notes or description",
            "manufacturer": "Manufacturer of the software/license",
            "purchase_date": "Date when the license was purchased",
            "expiry_date": "Expiration date of the license",
            "volume_type": "Single, volume, or unlimited use",
            "volume_limit": "Number of uses (if volume license)",
            "parent_license": "Link to a parent license if this is a child",
        }

    def clean(self):
        super().clean()
        # You can add any custom validation logic here


class LicenseBulkEditForm(forms.ModelForm):
    class Meta:
        model = License
        fields = [
            "name", "description", "manufacturer", "purchase_date",
            "expiry_date", "volume_type", "volume_limit", "parent_license",
        ]


class LicenseForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label="License Manufacturer",
        selector=True,
        quick_add=True
    )

    parent_license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="Parent License",
        help_text="Select a parent license if applicable.",
        selector=True,
        query_params={'manufacturer_id': '$manufacturer'}
    )

    license_key = forms.CharField(
        required=True,
        label="License Key"
    )

    name = forms.CharField(
        required=True,
        label="Name"
    )

    volume_type = forms.ChoiceField(
        choices=License.VOLUME_TYPE_CHOICES,
        required=True,
        label="Volume Type"
    )

    purchase_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Purchase Date"
    )

    expiry_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Expiry Date"
    )

    comment = CommentField()

    class Meta:
        model = License
        fields = [
            "manufacturer", "name", "license_key", "product_key", "serial_number", "description",
            "volume_type", "volume_limit", "parent_license",
            "purchase_date", "expiry_date", "comment"
        ]

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data:
            return cleaned_data

        volume_type = cleaned_data.get("volume_type")
        volume_limit = cleaned_data.get("volume_limit")

        if volume_type == "SINGLE":
            cleaned_data["volume_limit"] = 1
        elif volume_type == "UNLIMITED":
            cleaned_data["volume_limit"] = None
        elif volume_type == "VOLUME":
            if volume_limit is None or volume_limit < 2:
                self.add_error("volume_limit", "Volume licenses require a volume limit of at least 2.")

        return cleaned_data



class LicenseAssignmentForm(NetBoxModelForm):
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=True,
        label="License Manufacturer",
        selector=True,
        quick_add=True
    )

    license = DynamicModelChoiceField(
        queryset=License.objects.none(),
        required=True,
        label="License",
        selector=True,
        query_params={
            'manufacturer_id': '$manufacturer'
        }
    )

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Device",
        selector=True
    )

    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label="Virtual Machine",
        selector=True
    )

    comments = CommentField()

    fieldsets = (
        FieldSet("manufacturer", "license", "volume", "description", name="General Information"),
        FieldSet(
            TabbedGroups(
                FieldSet("device", name="Device Assignment"),
                FieldSet("virtual_machine", name="Virtual Machine Assignment"),
            ),
            name="Assignment Type"
        ),
    )

    class Meta:
        model = LicenseAssignment
        fields = [
            "manufacturer", "license", "device", "virtual_machine",
            "volume", "description", "comments"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        manufacturer = (
            self.data.get("manufacturer")
            or self.initial.get("manufacturer")
            or getattr(self.instance, "manufacturer", None)
        )

        if manufacturer:
            self.fields["license"].queryset = License.objects.filter(manufacturer=manufacturer)

        if self.instance.pk:
            self.fields["manufacturer"].disabled = True
            self.fields["license"].disabled = True
            self.fields["device"].disabled = True
            self.fields["virtual_machine"].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data:
            return cleaned_data

        device = cleaned_data.get("device")
        virtual_machine = cleaned_data.get("virtual_machine")
        license_obj = cleaned_data.get("license")

        if not device and not virtual_machine:
            raise forms.ValidationError("You must assign the license to either a Device or a Virtual Machine.")

        if device and virtual_machine:
            raise forms.ValidationError("You can only assign a license to either a Device or a Virtual Machine, not both.")

        if license_obj:
            license_obj.is_child_license = bool(license_obj.parent_license)
            license_obj.is_parent_license = license_obj.sub_licenses.exists()

        return cleaned_data

    def save(self, commit=True):
        assignment = super().save(commit=False)

        if self.cleaned_data.get("virtual_machine"):
            assignment.virtual_machine = self.cleaned_data["virtual_machine"]
            assignment.device = None
        elif self.cleaned_data.get("device"):
            assignment.device = self.cleaned_data["device"]
            assignment.virtual_machine = None

        if commit:
            assignment.save()

        return assignment


class LicenseAssignmentImportForm(NetBoxModelImportForm):
    manufacturer = CSVModelChoiceField(
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
        label='Manufacturer',
        help_text='The license manufacturer'
    )

    license = CSVModelChoiceField(
        queryset=License.objects.all(),
        to_field_name='license_key',
        label='License',
        help_text='Assigned license (by license key)'
    )

    device = CSVModelChoiceField(
        queryset=Device.objects.all(),
        to_field_name='name',
        required=False,
        label='Device',
        help_text='Device to assign the license to (optional)'
    )

    virtual_machine = CSVModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        to_field_name='name',
        required=False,
        label='Virtual Machine',
        help_text='Virtual machine to assign the license to (optional)'
    )

    class Meta:
        model = LicenseAssignment
        fields = ["manufacturer", "license", "device", "virtual_machine", "volume", "description"]
        labels = {
            "manufacturer": "Manufacturer",
            "license": "License",
            "device": "Device",
            "virtual_machine": "Virtual Machine",
            "volume": "Volume",
            "description": "Description",
        }
        help_texts = {
            "manufacturer": "The license manufacturer",
            "license": "License assigned by license key",
            "device": "Device name (if applicable)",
            "virtual_machine": "VM name (if applicable)",
            "volume": "How many units are assigned",
            "description": "Optional description of the assignment",
        }

    def clean(self):
        super().clean()
        device = self.cleaned_data.get("device")
        virtual_machine = self.cleaned_data.get("virtual_machine")

        if not device and not virtual_machine:
            raise forms.ValidationError("You must assign the license to either a Device or a Virtual Machine.")

        if device and virtual_machine:
            raise forms.ValidationError("A license can only be assigned to a Device or a Virtual Machine, not both.")

class LicenseAssignmentBulkEditForm(forms.ModelForm):
    class Meta:
        model = LicenseAssignment
        fields = ["license", "device", "volume", "description"]


class LicenseAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = LicenseAssignment
    filterset_class = LicenseAssignmentFilterSet

    manufacturer_id = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="License Manufacturer",
    )

    device_manufacturer_id = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="Device Manufacturer"
    )

    virtual_machine__cluster_id = DynamicModelMultipleChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        label="Cluster"
    )

    license = DynamicModelChoiceField(
        queryset=License.objects.all(),
        required=False,
        label="License",
        query_params={'manufacturer_id': '$manufacturer_id'}
    )

    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label="Device"
    )

    virtual_machine_id = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        label="Virtual Machine"
    )

    comments = CommentField()

    class Meta:
        model = LicenseAssignment
        fields = [
            "manufacturer_id", "device_manufacturer_id", "cluster_id",
            "device_id", "virtual_machine_id", "license", "assigned_to", "volume", "comments"
        ]