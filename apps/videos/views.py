from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CommentForm, CustomForm
from .models import Videos, Comments, LikeDislike
from apps.accounts.models import User, Subscription


class VideoCreateView(CreateView):
    model = Videos
    fields = ['title', 'description', 'video_file', 'image']
    template_name = 'video_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('video_list')


@login_required
def video_update(request, url):
    video = get_object_or_404(Videos, url=url, author=request.user)

    if request.method == 'POST':
        form = CustomForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('video_view', url=video.url)
    else:
        form = CustomForm(instance=video)

    return render(request, 'video_update.html', {'form': form, 'video': video})


@login_required
def video_delete(request, url):
    video = get_object_or_404(Videos, url=url, author=request.user)

    if request.method == 'POST':
        video.image.delete()
        video.video_file.delete()
        video.delete()
        return redirect('my_videos')

    return render(request, 'video_delete.html', {'video': video})


def video_list(request):
    videos_list = Videos.objects.all()
    return render(request, 'video_list.html', {'videos': videos_list})


def video_view(request, url):
    video = Videos.objects.get(url=url)

    video_author = User.objects.get(id=video.author_id).username
    channel_user = video.author
    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = Subscription.objects.filter(subscriber=request.user, channel_user=channel_user).exists()
    comments = Comments.objects.filter(video=video)
    comments_count = Comments.objects.count()

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.video = video
                comment.user_id = request.user.id
                comment.save()
        action = request.POST.get('action')
        if request.user.is_authenticated:
            if action == 'like':
                if video.votes.filter(user=request.user, vote=LikeDislike.LIKE).exists():
                    # Если пользователь уже поставил лайк, удаляем его
                    video.votes.filter(user=request.user, vote=LikeDislike.LIKE).delete()
                else:
                    # Если пользователь не поставил лайк, добавляем его
                    video.votes.create(user=request.user, vote=LikeDislike.LIKE)
                    if video.votes.filter(user=request.user, vote=LikeDislike.DISLIKE).exists():
                        video.votes.filter(user=request.user, vote=LikeDislike.DISLIKE).delete()
            elif action == 'dislike':
                # Аналогичные действия для дизлайка
                if video.votes.filter(user=request.user, vote=LikeDislike.DISLIKE).exists():
                    video.votes.filter(user=request.user, vote=LikeDislike.DISLIKE).delete()
                else:
                    video.votes.create(user=request.user, vote=LikeDislike.DISLIKE)
                    if video.votes.filter(user=request.user, vote=LikeDislike.LIKE).exists():
                        video.votes.filter(user=request.user, vote=LikeDislike.LIKE).delete()
            elif action == 'unlike':
                likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(video),
                                                      object_id=video.id, user=request.user)
                likedislike.delete()
    else:
        comment_form = CommentForm()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        like_count = video.votes.filter(vote=LikeDislike.LIKE).count()
        dislike_count = video.votes.filter(vote=LikeDislike.DISLIKE).count()
        return JsonResponse({
            'like_count': like_count,
            'dislike_count': dislike_count,
        })
    else:
        video.view_count += 1
        video.save()
        like_count = video.votes.filter(vote=LikeDislike.LIKE).count()
        dislike_count = video.votes.filter(vote=LikeDislike.DISLIKE).count()
        context = {
            'video': video,
            'video_author': video_author,
            'comments': comments,
            'comment_form': comment_form,
            'comments_count': comments_count,
            'like_count': like_count,
            'dislike_count': dislike_count,
            'is_subscribed': is_subscribed,
        }
        return render(request, 'video_view.html', context)


def my_videos_list(request):
    my_videos = Videos.objects.filter(author_id=request.user.id).order_by('uploaded_at')
    context = {
        'my_videos': my_videos
    }

    return render(request, 'my_videos.html', context)


def my_liked_videos_list(request):
    likes = LikeDislike.objects.filter(user_id=request.user.id)
    liked_videos = Videos.objects.filter(id__in=[like.object_id for like in likes])
    context = {
        'liked_videos': liked_videos
    }

    return render(request, 'liked_videos.html', context)


def video_search(request):
    query = request.GET.get('query', '')
    videos = Videos.objects.filter(title__icontains=query)
    context = {
        'videos': videos,
        'query': query,
    }
    return render(request, 'video_search.html', context)


def channel_videos(request, username):
    channel_user = User.objects.get(username=username)
    videos = Videos.objects.filter(author=channel_user).order_by('uploaded_at')
    is_subscribed = Subscription.objects.filter(subscriber=request.user, channel_user=channel_user).exists()
    context = {'channel_user': channel_user, 'videos': videos, 'is_subscribed': is_subscribed}
    return render(request, 'channel_videos.html', context)
