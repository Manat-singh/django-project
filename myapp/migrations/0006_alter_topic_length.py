# Generated by Django 3.2.13 on 2022-07-31 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_topic_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='length',
            field=models.IntegerField(default=1),
        ),
    ]
