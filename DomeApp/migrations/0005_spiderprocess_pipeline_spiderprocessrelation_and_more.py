# Generated by Django 4.1.4 on 2022-12-30 23:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DomeApp', '0004_spider_slug_alter_spider_spy_spidercall'),
    ]

    operations = [
        migrations.AddField(
            model_name='spiderprocess',
            name='pipeline',
            field=models.CharField(default='', max_length=300, verbose_name='pipeline name'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='SpiderProcessRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DomeApp.spiderprocess')),
                ('spider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DomeApp.spider')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('order', 'spider', 'process')},
            },
        ),
        migrations.AddField(
            model_name='spider',
            name='processes',
            field=models.ManyToManyField(related_name='spider_processes', through='DomeApp.SpiderProcessRelation', to='DomeApp.spiderprocess'),
        ),
    ]
