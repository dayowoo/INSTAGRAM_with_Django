from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import auth
from .models import *
from post.views import *
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.http import HttpResponse
from django.contrib import messages

# 회원가입
def sign_up(request):
    if request.method == "GET":
        return render(request, "sign_up.html")
    elif request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        password_check = request.POST["pw_check"]
        image = request.FILES["image"]
        # 비밀번호 재확인 불일치
        if password != password_check:
            return render(request, "sign_up.html")
        # 새로운 유저 생성
        user = User.objects.create_user(username=username, password=password, name=name, email=email, image=image)
        auth.login(request, user)
    return redirect('main')

# 로그인
def sign_in(request):
    if request.method == "GET":
        return render(request, "sign_in.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        # 존재하지 않는 user
        if user is None:
            return render(request, "sign_in.html")
        # 로그인 처리
        auth.login(request, user)
    return redirect("main")

# 로그아웃
def sign_out(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            auth.logout(request)
    return redirect('main')

# 프로필
@login_required
def profile(requset,username):
    user = get_object_or_404(User,username=username)
    post_list = user.post_set.all()
    return render(requset, "profile.html",{ "user_profile":user,'post_list': post_list,'username': username})

@login_required
@require_POST
def follow(request):
    from_user = request.user
    pk = request.POST.get('pk')
    to_user = get_object_or_404(User, pk=pk)
    relation, created = Relation.objects.get_or_create(from_user=from_user, to_user=to_user)

    if created:
        message = '팔로우 시작!'
        status = 1
    else:
        relation.delete()
        message = '팔로우 취소'
        status = 0

    context = {
        'message': message,
        'status': status,
    }
    return HttpResponse(json.dumps(context), content_type="application/json")