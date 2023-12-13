from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from .models import Channel, Video, Comment

# Create your views here.
def home(request):
    videos = Video.objects.all().order_by('-upload_time')

    return render(request, "home.html", {"videos":videos})

def channel(request, username,pk):
    user = User.objects.get(username=username)
    channel = Channel.objects.get(user=user, id=pk)
    videos = Video.objects.filter(channel=channel).order_by('-upload_time')

    if request.method == "POST":
        action = request.POST['subscribe']

        if action == 'unsubscribe':
            channel.subscribers.remove(request.user)
        else:
            channel.subscribers.add(request.user)

        channel.save()

    return render(request, "channel.html", {"channel":channel, "videos":videos})

def video(request, pk):
    video = Video.objects.get(id=pk)
    return render(request, "video.html", {"video":video})

def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, "create_user.html", {'form':form})

def custom_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')

    else:
        return render(request, "login.html")

def custom_logout(request):
    logout(request)
    return redirect('home')

def create_channel(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST["channelName"]
            pfp = request.FILES.get('channel_pfp')

            if name and pfp:
                channel = Channel(user=request.user, name=name, profile_picture=pfp)
                channel.save()

                return redirect('home')
        else:
            return render(request, 'create_channel.html')
    
    else:
        return redirect('login')
    
    return render(request, 'create_channel.html')

def upload_video(request):
    if request.user.is_authenticated:
        channels = Channel.objects.filter(user=request.user)

        if request.method == "POST":
            channel_id = request.POST['video_channel']

            channel = Channel.objects.get(id=channel_id)

            video_file = request.FILES.get('video_file')
            title = request.POST['video_title']
            description = request.POST['video_description']
            thumbnail = request.FILES.get('video_thumbnail')

            if channel and video_file and title and thumbnail:
                video = Video(user=request.user, channel=channel, video_file=video_file, title=title, description=description, thumbnail=thumbnail)
                video.save()

                return redirect('home')

        else:
            return render(request, "upload_video.html", {"channels":channels})

    else:
        return redirect('login')

    return render(request, "upload_video.html", {"channels":channels})

def searched(request):
    if request.method == "POST":
        searched_value = request.POST['s']
        videos = Video.objects.filter(title__contains=searched_value)
        channels = Channel.objects.filter(name__contains=searched_value)

        return render(request, "searched.html", {"videos":videos, "channels":channels})

def video_view(request, pk):
    if request.user.is_authenticated:
        video = Video.objects.get(id=pk)

        if not video.view.filter(id=request.user.id):
            video.view.add(request.user)
        
        return redirect('video', pk=pk)
    else:
        return redirect('login')

def video_like(request, pk):
    if request.user.is_authenticated:
        video = Video.objects.get(id=pk)

        if not video.dislikes.filter(id=request.user.id):
            if video.likes.filter(id=request.user.id):
                video.likes.remove(request.user)
            else:
                video.likes.add(request.user)
        
        return redirect('video', pk=pk)
    
    else:
        return redirect('login')

def video_dislike(request, pk):
    if request.user.is_authenticated:
        video = Video.objects.get(id=pk)

        if not video.likes.filter(id=request.user.id):
            if video.dislikes.filter(id=request.user.id):
                video.dislikes.remove(request.user)
            else:
                video.dislikes.add(request.user)
        
        return redirect('video', pk=pk)
    
    else:
        return redirect('login')

def video_comment(request, pk):
    if request.user.is_authenticated:
        video = Video.objects.get(id=pk)

        if request.method == "POST":
            comment_text = request.POST['comment']
            comment = Comment.objects.create(user=request.user, video=video, text=comment_text)

        return redirect('video', pk=pk)

    else:
        return redirect('login')
