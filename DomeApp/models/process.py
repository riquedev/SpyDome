import inspect
from django.db import models
from django_extensions.db.models import TimeStampedModel, ActivatorModel
from django.utils.translation import gettext as _
from DomeApp.dome.dome import pipelines
from DomeApp.dome.dome.pipelines.base import BaseSpyPipeline

_pipeline_tuples = tuple(filter(lambda member: inspect.isclass(member[1]), inspect.getmembers(pipelines)))
_pipeline_names = list(map(lambda pipe: pipe[0], _pipeline_tuples))
_pipeline_dict = dict({item[0]: item[1] for item in _pipeline_tuples})


class PipelineNotExists(Exception):
    pass


class SpiderProcess(TimeStampedModel, ActivatorModel):
    name = models.CharField(max_length=300, verbose_name=_("spider process name"))
    pipeline = models.CharField(max_length=300, verbose_name=_("pipeline name"))
    params = models.JSONField(default=dict, blank=True, null=True)

    @classmethod
    def get_available_pipelines(cls):
        return _pipeline_names

    @classmethod
    def get_pipeline_description(cls, pipeline):
        return cls._get_pipeline(pipeline, instance=False).__doc__

    @classmethod
    def get_html_description(cls, pipeline) -> BaseSpyPipeline:
        return cls._get_pipeline(pipeline, instance=False).__html__

    def save(self, **kwargs):
        assert self.pipeline in _pipeline_names
        return super().save(**kwargs)

    @classmethod
    def _get_pipeline(cls, name: str, instance: bool = True) -> BaseSpyPipeline:
        obj = _pipeline_dict.get(name, None)

        if obj is None:
            raise PipelineNotExists(f"{name} not found, only: {', '.join(_pipeline_names)} are available")

        if instance:
            obj = obj()

        return obj

    @property
    def python_object(self) -> BaseSpyPipeline:
        return self._get_pipeline(self.pipeline)

    class Meta:
        unique_together = ('name', 'spider')
