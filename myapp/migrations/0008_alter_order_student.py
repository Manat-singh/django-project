# Generated by Django 4.0.5 on 2022-08-05 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_merge_20220803_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.student'),
        ),
    ]
