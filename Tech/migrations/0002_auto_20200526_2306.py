# Generated by Django 3.0.5 on 2020-05-26 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tech', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scontents',
            name='SCName',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
