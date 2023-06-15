from django.urls import path, re_path
from .views import VideoCreateView, video_list, video_view, my_videos_list, video_update, \
    my_liked_videos_list, video_search, video_delete, channel_videos


urlpatterns = [
    path('', video_list, name='video_list'),
    path('create/', VideoCreateView.as_view(), name='video_create'),
    path('videos/<str:url>/edit/', video_update, name='video_update'),
    path('videos/<str:url>/delete/', video_delete, name='video_delete'),
    re_path(r'^(?P<url>watch\.v\..+)$', video_view, name='video_view'),
    path('search/', video_search, name='video_search'),
    path('account/my_videos', my_videos_list, name='my_videos'),
    path('account/liked_videos', my_liked_videos_list, name='liked_videos'),
    path('channel/<str:username>/', channel_videos, name='channel_videos'),
]
