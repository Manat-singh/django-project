# Generated by Django 4.0.5 on 2022-07-30 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_passwordreset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='myapp.student'),
        ),
    ]