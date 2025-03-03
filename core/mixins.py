import os
from django.conf import settings
from core.models import *


class DataProviderMixin:
    def get_data(self):
        data = {
            "journal": Journal.objects.all().first(),
            "policies": Policy.objects.all().order_by("name"),
            "ads": AdConfig.get_solo()
        }
        return data
