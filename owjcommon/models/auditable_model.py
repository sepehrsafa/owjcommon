from tortoise.models import Model
from tortoise import fields
import uuid
from ..exceptions import OWJException
from ..enums import AuditTypeEnum


class AuditableModel(Model):
    audit_log_class: Model = None

    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.audit_log_class is None:
            raise TypeError(
                "Subclasses of AuditableModel must provide an audit_log_class."
            )

    async def log_changes(self, instance, model_pk, type, changes, user=None):
        # check user type if string or object
        if user:
            if isinstance(user, str):
                user = user
            else:
                user = user.uuid

        audit_log = self.audit_log_class()
        await audit_log.create(
            model_name=instance.__class__.__name__,
            model_pk=model_pk,
            type=type,
            changes=changes,
            changed_by_id=user,
        )

    async def save(self, *args, user=None, **kwargs):
        changes = {}
        new_instance = False

        original_instance = await type(self).get_or_none(pk=self.pk)
        if original_instance:
            for field in self._meta.fields_map.keys():
                original_value = getattr(original_instance, field)
                current_value = getattr(self, field)
                # check if original value or current value is of type tortoise.fields.relational.ReverseRelation and skip
                if isinstance(
                    original_value, fields.relational.ReverseRelation
                ) or isinstance(current_value, fields.relational.ReverseRelation):
                    continue

                # check if any of the values is of tpye tortoise.fields.relational._NoneAwaitable and put None in changes
                if isinstance(original_value, fields.relational._NoneAwaitable):
                    original_value = None
                if isinstance(current_value, fields.relational._NoneAwaitable):
                    current_value = None

                # check if object of tortoise model and get pk
                if isinstance(original_value, Model):
                    original_value = original_value.pk
                if isinstance(current_value, Model):
                    current_value = current_value.pk

                # if foreign key field then get pk
                if isinstance(
                    original_value, fields.relational.ForeignKeyFieldInstance
                ):
                    original_value = getattr(original_instance, f"{field}_id")
                if isinstance(current_value, fields.relational.ForeignKeyFieldInstance):
                    current_value = getattr(self, f"{field}_id")

                if original_value != current_value:
                    changes[field] = {
                        "old": str(original_value),
                        "new": str(current_value),
                    }
        else:
            new_instance = True
            for field in self._meta.fields_map.keys():
                current_value = getattr(self, field)
                changes[field] = {"old": None, "new": str(current_value)}

        await super().save(*args, **kwargs)
        if changes and new_instance:
            await self.log_changes(
                self, self.pk, AuditTypeEnum.CREATE, changes, user=user
            )
        elif changes:
            await self.log_changes(
                self, self.pk, AuditTypeEnum.UPDATE, changes, user=user
            )

    @classmethod
    async def get_or_exception(cls, *args, **kwargs):
        prefetch_related = kwargs.pop("prefetch_related", None)
        print(prefetch_related)
        if prefetch_related:
            data = await cls.get_or_none(*args, **kwargs).prefetch_related(
                *prefetch_related
            )
        else:
            data = await cls.get_or_none(*args, **kwargs)
        if data is None:
            raise OWJException("E1023", 404)
        return data
