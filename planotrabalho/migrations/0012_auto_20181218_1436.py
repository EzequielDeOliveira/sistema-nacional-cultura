# Generated by Django 2.0.8 on 2018-12-18 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planotrabalho', '0011_auto_20181206_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conselheiro',
            name='conselho',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planotrabalho.Componente', null=True),
        ),
    ]