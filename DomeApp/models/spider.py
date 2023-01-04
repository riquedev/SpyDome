import pathlib
import os
import subprocess
import threading
from datetime import datetime
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models, connection
from django.db.models import QuerySet
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TimeStampedModel, ActivatorModel
from django.utils.translation import gettext as _
from django.dispatch import receiver
from .urls import SpyURL
from .process import SpiderProcess
from DomeApp.signals import spy_finished


# Methods
def spider_call_upload_to(instance: 'SpiderCall', file_name: str) -> str:
    return str(pathlib.Path('spider_call') / instance.spider.slug / str(instance.pk) / file_name)


class Spider(TimeStampedModel, ActivatorModel):
    """
    Spider's main model, here we have all the necessary relationships
    to run our Spider, it's also where we centralize the build methods.
    """

    class Spy(models.TextChoices):
        DEFAULT = 'spy', _("Default")

    auth = models.ForeignKey('SpiderAuthentication', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=300, verbose_name=_("spider name"))
    slug = AutoSlugField(populate_from=['name'])
    custom_settings = models.JSONField(default=dict)
    start_urls = models.ManyToManyField(SpyURL, through='SpiderStartUrl')
    processes = models.ManyToManyField(SpiderProcess, through='SpiderProcessRelation', related_name='spider_processes')
    spy = models.TextField(choices=Spy.choices, default=Spy.DEFAULT)

    @property
    def results(self) -> QuerySet['SpiderResult']:
        return self.spiderresult_set.all()

    @property
    def last_result(self):
        return self.results.last()

    @property
    def ordered_start_urls(self) -> QuerySet[SpyURL]:
        return self.start_urls.order_by('spiderstarturl__order')

    @property
    def ordered_processes(self) -> QuerySet[SpiderProcess]:
        return self.processes.order_by('spiderprocessrelation__order')

    @property
    def crawl_args(self) -> list:
        return ['scrapy', 'crawl', self.spy, '-a', f'id={self.pk}']

    def _initialize(self, call_id: int, testing: bool = False):
        os.environ['TEST'] = 'True' if testing else 'False'
        call = SpiderCall.objects.get(pk=call_id)
        args = self.crawl_args

        if testing:
            args += ['-a', 'testing=1']

        call.args = args
        call.save()
        current_dir = os.getcwd()
        os.chdir(settings.SPY_FOLDER)

        connection.commit()
        process = subprocess.Popen(args, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, encoding="utf-8")
        output, error = process.communicate()
        os.chdir(current_dir)

        spy_finished.send(sender=self, output=output, error=error, call=call)

    def initialize(self, is_test: bool = False):
        call = SpiderCall.objects.create(spider=self)
        call.save()
        thread = call

        if not is_test:
            thread = threading.Thread(target=self._initialize, args=(call.pk, is_test))
            thread.setDaemon(True)
            thread.start()

        return thread


class SpiderStartUrl(models.Model):
    """
    Relation between Spider and SpyURL.
    It is necessary for us to be able to create an "order" of execution.
    """
    order = models.PositiveIntegerField()
    spider = models.ForeignKey('Spider', on_delete=models.CASCADE)
    url = models.ForeignKey('SpyURL', on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']
        unique_together = ('order', 'spider', 'url')


class SpiderProcessRelation(models.Model):
    """
    Relation between Spider and SpiderProcess.
    It is necessary for us to be able to create an "order" of execution.
    """
    order = models.PositiveIntegerField()
    spider = models.ForeignKey('Spider', on_delete=models.CASCADE)
    process = models.ForeignKey('SpiderProcess', on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']
        unique_together = ('order', 'spider', 'process')


class SpiderCall(TimeStampedModel):
    """
    Model responsible for storing Spider's post-execution details.
    """
    spider = models.ForeignKey('Spider', on_delete=models.CASCADE)
    args = models.JSONField(default=list)
    return_code = models.IntegerField(null=True, blank=True)
    stdout = models.FileField(upload_to=spider_call_upload_to)
    stderr = models.FileField(upload_to=spider_call_upload_to)


@receiver(spy_finished)
def on_spy_finished(sender: Spider, **kwargs):
    output = kwargs['output']
    error = kwargs['error']
    call = kwargs['call']

    assert isinstance(output, str)
    assert isinstance(error, str)
    assert isinstance(call, SpiderCall)
    ts = datetime.now().utcnow()
    call.stdout.save(f'stdout-{ts}.log', ContentFile(output))
    call.stderr.save(f'stderr-{ts}.log', ContentFile(error))
