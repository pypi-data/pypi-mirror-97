import datetime
from decimal import Decimal
from uuid import UUID
from typing import Tuple, List
from django.db.models import ManyToManyField
from django.db.models.fields import Field
from pydantic import IPvAnyAddress, Json
from pydantic.fields import FieldInfo


TYPES = {
    "AutoField": int,
    "BigIntegerField": int,
    "BinaryField": bytes,
    "BooleanField": bool,
    "CharField": str,
    "DateField": datetime.date,
    "DateTimeField": datetime.datetime,
    "DecimalField": Decimal,
    "DurationField": datetime.timedelta,
    "FileField": str,
    "FilePathField": str,
    "FloatField": float,
    "GenericIPAddressField": IPvAnyAddress,
    "IPAddressField": IPvAnyAddress,
    "IntegerField": int,
    "JSONField": Json,
    "NullBooleanField": bool,
    "PositiveBigIntegerField": int,
    "PositiveIntegerField": int,
    "PositiveSmallIntegerField": int,
    "SlugField": str,
    "SmallIntegerField": int,
    "TextField": str,
    "TimeField": datetime.time,
    "UUIDField": UUID,
}


def create_m2m_link_type(type_):
    class M2MLink(type_):
        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def validate(cls, v):
            return v.pk

    return M2MLink


def get_schema_field(field: Field, *, depth: int = 0) -> Tuple:
    alias = None
    default = ...
    default_factory = None
    description = None
    title = None
    max_length = None
    python_type = None

    if field.is_relation:
        if depth > 0:
            return get_related_field_schema(field, depth=depth)

        internal_type = field.related_model._meta.pk.get_internal_type()

        if not field.concrete and field.auto_created or field.null:
            default = None

        if hasattr(field, "get_attname"):
            alias = field.get_attname()

        pk_type = TYPES.get(internal_type, int)
        if field.one_to_many or field.many_to_many:
            m2m_type = create_m2m_link_type(pk_type)
            python_type = List[m2m_type]
        else:
            python_type = pk_type

    else:
        field_options = field.deconstruct()[3]  # 3 are the keywords
        blank = field_options.get("blank", False)
        null = field_options.get("null", False)
        max_length = field_options.get("max_length")

        internal_type = field.get_internal_type()
        python_type = TYPES[internal_type]

        if field.has_default():
            if callable(field.default):
                default_factory = field.default
            else:
                default = field.default
        elif field.primary_key or blank or null:
            default = None

    description = field.help_text
    title = field.verbose_name.title()

    return (
        python_type,
        FieldInfo(
            default,
            alias=alias,
            default_factory=default_factory,
            title=title,
            description=description,
            max_length=max_length,
        ),
    )


def get_related_field_schema(field: Field, *, depth: int):
    from ninja.orm import create_schema

    model = field.related_model
    schema = create_schema(model, depth=depth - 1)
    default = ...
    if not field.concrete and field.auto_created or field.null:
        default = None
    if isinstance(field, ManyToManyField):
        schema = List[schema]

    return (
        schema,
        FieldInfo(
            default=default,
            description=field.help_text,
            title=field.verbose_name.title(),
        ),
    )
