# Generated by Django 3.1.4 on 2020-12-31 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nearby', '0003_auto_20201230_1727'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nearbycomment',
            old_name='user',
            new_name='uploader',
        ),
    ]