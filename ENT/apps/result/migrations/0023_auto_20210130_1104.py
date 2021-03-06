# Generated by Django 3.1.5 on 2021-01-30 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0022_auto_20210129_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='result.person'),
        ),
        migrations.AlterField(
            model_name='target',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='result.person'),
        ),
        migrations.AlterField(
            model_name='tragetent',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='result.person'),
        ),
        migrations.AlterField(
            model_name='trial',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='result.person'),
        ),
        migrations.AlterField(
            model_name='trialsub',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='result.person'),
        ),
    ]
