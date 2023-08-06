from pathlib import Path

from django.apps import AppConfig


class DjAppConfig(AppConfig):
    name = Path(__file__).parent.stem
