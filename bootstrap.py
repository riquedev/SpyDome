import os
import django


def init_bootstrap():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SpyDome.settings")
    django.setup()

