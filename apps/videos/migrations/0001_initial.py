# Generated by Django 4.2 on 2023-05-15 05:12

from django.db import migrations, models
import apps.videos.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('videos', models.FileField(upload_to='videos/', validators=[apps.videos.validators.validate_video_extension])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]