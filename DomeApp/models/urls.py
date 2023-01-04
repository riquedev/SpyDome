from django.db import models
from django_extensions.db.models import TimeStampedModel, ActivatorModel


class SpyURL(TimeStampedModel, ActivatorModel):
    """
    Model responsible for storing the url's used by the Dome,
    in the future we want to add some useful methods here,
    for example to enable the cache of a url and also to
    store details in properties, an example of this would
    be the title of the page, without the need to go through a Beautifulsoup a second time.
    """
    url = models.URLField()
