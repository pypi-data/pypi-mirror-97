import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import JSONField

from helpers.validators import locale_regex

class Base(models.Model):
    INVISIBLE = 0
    VISIBLE = 1
    INACTIVE = 2
    DELETED = 3

    STATUS_CHOICES = [
        (INVISIBLE, 'Invisible'),
        (VISIBLE, 'Visible'),
        (INACTIVE, 'Inactive'),
        (DELETED, 'Deleted'),
    ]

    claims_rules = JSONField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=191, blank=True, null=True)
    created_by = models.CharField(max_length=191, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    hero = models.BooleanField(blank=True, null=True)
    order_number = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=VISIBLE,
        verbose_name='Status',
        validators=[MinValueValidator(0), MaxValueValidator(3)],
    )
    client = JSONField(blank=True, null=True)

    class Meta:
        abstract = True


class Locale(Base):

    locale = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        validators=[locale_regex,]
    )

    class Meta:
        abstract = True
