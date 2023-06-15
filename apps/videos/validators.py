from django.core.exceptions import ValidationError
import os


def validate_video_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4', '.avi', '.mov']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Формат видео-файла не поддерживается. Допустимые форматы: %s' % ", ".join(valid_extensions))