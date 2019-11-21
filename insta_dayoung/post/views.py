from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.utils import timezone
from .models import *
from account.models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import auth
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import re
from django.contrib import messages

def main(request):
    posts = Post.objects.prefetch_related('hashtags').select_related('author').all()
    return render(request, 'main.html',{"posts":posts})

@login_required
def create(request):
    if request.method=="POST":
        form = NewPost(request.POST, request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.created_at = timezone.now()
            post.author=request.user
            post.save()
            content = form.cleaned_data.get('content')
            content_words = content.split()
            for word in content_words :
                if word[0] == "#" :
                    tag = Hashtag.objects.get_or_create(content=word)
                    post.hashtags.add(tag[0])
            return redirect("main")
    elif request.method=="GET":
        form = NewPost()
        return render(request, "post_new.html",{"form":form})

def hashtags(request, hashtag_id):
    hashtag = Hashtag.objects.get(id=hashtag_id)
    posts = hashtag.post_set.order_by('-id')
    context={'posts':posts,'hashtag':hashtag}
    return render(request, 'hashtags.html', context)


@require_POST
def like(request):
    id = request.POST.get('pk', None) 
    post = get_object_or_404(Post, pk=id)
    post_like, post_like_created = post.like_set.get_or_create(username=request.user)

    if not post_like_created:
        post_like.delete()
        message = "좋아요 취소"
    else:
        message = "좋아요"

    context = {'like_count': post.like_count,
               'message': message,
                }

    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def update(request,id):
    if request.method == "GET":
        post = get_object_or_404(Post, pk=id)
        form = NewPost(instance=post)
        return render(request, "post_edit.html",{"form":form, "post":post})
    elif request.method == "POST":
        post = get_object_or_404(Post, pk=id)
        form = NewPost(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.created_at = timezone.now()
            post.save()
                        # cleaned_data저장된 값을 가져온다?
            content = form.cleaned_data.get('content')
            #split 나누기
            content_words = content.split()
            for word in content_words :
                if word[0] == "#" :
                    tag = Hashtag.objects.get_or_create(content=word)
                    post.hashtags.add(tag[0])
        return redirect("main")
    return Http404()

@login_required
def delete(request,id):
    post=get_object_or_404(Post,pk=id)
    if post.author != request.user:
        return redirect("main")
    post.delete()
    return redirect("main")


def my_post_list(request,username):
    user = get_object_or_404(User,username=username)
    post_list = user.post_set.all()
    return render(request, "my_post_list.html",{ "user_profile":user,'post_list': post_list,'username': username})



@login_required
def my_detail(request,id):
    # user = get_object_or_404(User, pk=id)
    post = get_object_or_404(Post, pk=id)
    # posts = Post.objects.prefetch_related('hashtags').select_related('author').all()
    return render(request,"my_detail.html",{'post':post})



@login_required
def follow_list(request):
    follows = request.user.get_following
    posts = Post.objects.filter(author__in=follows)
    if request.is_ajax(): 
        return render(request, 'main.html', {
            'posts': posts
        })

    return render(request, 'main.html', {
        'follows': follows,
        'posts': posts
    })



def search_list(request):
    hashtag = Hashtag.objects.filter(content=request.GET["search"]).first()
    user = User.objects.filter(username=request.GET["search"]).first()
    if hashtag:
        posts = hashtag.post_set.order_by('-id')
        context = {'hashtag':hashtag,'posts':posts}
        return render(request, "hashtags.html",context)
    elif user:
        return redirect('my_post_list',request.user.username)
    else:
        return HttpResponse("검색한 내용이 없어 ㅡㅡ")
