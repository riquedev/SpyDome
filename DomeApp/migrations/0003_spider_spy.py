# Generated by Django 4.1.4 on 2022-12-30 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DomeApp', '0002_alter_spiderstarturl_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='spider',
            name='spy',
            field=models.CharField(choices=[('DF', 'Default')], default='DF', max_length=2),
        ),
    ]
