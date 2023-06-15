# Generated by Django 4.2 on 2023-06-14 09:27

import apps.videos.validators
from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0012_alter_likedislike_user_alter_likedislike_vote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videos',
            name='image',
            field=models.ImageField(storage=storages.backends.s3boto3.S3Boto3Storage(), upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='videos',
            name='video_file',
            field=models.FileField(storage=storages.backends.s3boto3.S3Boto3Storage(), upload_to='videos/', validators=[apps.videos.validators.validate_video_extension]),
        ),
    ]
