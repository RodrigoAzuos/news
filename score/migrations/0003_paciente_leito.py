# Generated by Django 2.0 on 2019-12-02 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0002_auto_20191202_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='leito',
            field=models.IntegerField(default=1, verbose_name='leito'),
            preserve_default=False,
        ),
    ]
