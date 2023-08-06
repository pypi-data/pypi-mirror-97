from django.db import models

from unchained_utils.v0.base_classes import unBaseModel, LooseForeignKey
from unchained_utils.v0 import g


class Currency(unBaseModel):
    id = models.CharField(max_length=3, primary_key=True)
    name_en = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100, null=True, blank=True)


class Country(unBaseModel):
    id = models.CharField(max_length=2, primary_key=True)
    name_en = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)

    @property
    def name(self):
        return self.name_ar if g.language == "ar" else self.name_en


class Region(unBaseModel):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=100, unique=True)
    country = LooseForeignKey(Country)
    name_en = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100, null=True, blank=True)

    @property
    def name(self):
        return self.name_ar if g.language == "ar" else self.name_en

    class Meta:
        unique_together = ('key', 'country')
