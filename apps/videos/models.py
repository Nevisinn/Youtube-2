import uuid

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from storages.backends.s3boto3 import S3Boto3Storage

from apps.videos.validators import validate_video_extension
from apps.accounts.models import User


class Videos(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', storage=S3Boto3Storage())
    video_file = models.FileField(upload_to='videos/', storage=S3Boto3Storage(), validators=[validate_video_extension],)
    url = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0)
    votes = GenericRelation('LikeDislike')


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTE_CHOICES = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)


@receiver(pre_save, sender=Videos)
def video_file_path(sender, instance, **kwargs):
    if not instance.url:
        instance.url = f'watch.v.{str(uuid.uuid4())[:16]}'


class Comments(models.Model):
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
