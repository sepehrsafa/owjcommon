# mypackage/audit.py
import uuid

from tortoise import fields
from tortoise.models import Model

from ..enums import AuditTypeEnum


class AuditLogBase(Model):
    uuid = fields.UUIDField(pk=True, default=uuid.uuid4)
    model_name = fields.CharField(max_length=255)
    model_pk = fields.CharField(max_length=255)
    type = fields.CharEnumField(AuditTypeEnum)
    changes = fields.JSONField()
    timestamp = fields.DatetimeField(auto_now_add=True)
    changed_by = fields.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = (
            True  # This makes sure that the base model itself is not created as a table
        )
