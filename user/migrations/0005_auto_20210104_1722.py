# Generated by Django 3.1.4 on 2021-01-04 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210102_0855'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address1',
            new_name='district',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='address2',
            new_name='neighborhood',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='address3',
            new_name='region',
        ),
    ]
