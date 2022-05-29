from django.db.models import (
    Model,
    CharField,
    BooleanField,
    JSONField,
)


class Product(Model):
    """
    Product model
    """
    is_active = BooleanField(default=True)
    name = CharField(max_length=50, unique=True)
    description = CharField(max_length=255)
    attributes = JSONField()

    def __str__(self):
        return self.name
