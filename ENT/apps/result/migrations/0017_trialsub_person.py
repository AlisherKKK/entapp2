# Generated by Django 3.1.5 on 2021-01-13 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0016_auto_20210113_2235'),
    ]

    operations = [
        migrations.AddField(
            model_name='trialsub',
            name='person',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='result.person'),
            preserve_default=False,
        ),
    ]
