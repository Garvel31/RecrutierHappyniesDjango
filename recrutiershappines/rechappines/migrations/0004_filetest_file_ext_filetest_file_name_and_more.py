# Generated by Django 4.0.1 on 2022-01-28 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rechappines', '0003_filetest'),
    ]

    operations = [
        migrations.AddField(
            model_name='filetest',
            name='file_ext',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='filetest',
            name='file_name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='filetest',
            name='file_path',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]