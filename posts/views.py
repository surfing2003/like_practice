from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Like

from django.contrib.auth.decorators import login_required

# Create your views here.
def new(request):
    return render(request, 'posts/new.html')


def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        writer = request.user
        image = request.FILES.get('image')
        Post.objects.create(title=title, content=content, writer=writer, image=image)
    return redirect('posts:main')


def main(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/main.html', {'posts': posts})


def show(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.view_count += 1
    post.save()
    all_comments = post.comments.all().order_by('-created_at')
    return render(request, 'posts/show.html', {'post': post, 'comments': all_comments })


def update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.image = request.FILES.get('image')
        post.save()
        return redirect('posts:show', post.id)
    return render(request, 'posts/edit.html', {"post": post})


def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('posts:main')


def create_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        current_user = request.user
        comment_content = request.POST.get('content')
        Comment.objects.create(content=comment_content, writer=current_user, post=post)
    return redirect('posts:show', post_id)

# 함수형 뷰에서만 사용가능한 사용자 로그인 여부 
@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post,pk=post_id)
    post_like, post_like_created = post.like_set.get_or_create(user=request.user)
    
    #좋아요 확인
    if not post_like_created:
        post_like.delete()

    #show, main 확인하고 redirect
    if request.GET.get('redirect_to') == 'show':
        return redirect('posts:show', post_id)
    elif request.GET.get('redirect_to') == 'like_list':
        return redirect('posts:like_list')
    else:
        return redirect('posts:main')

# @login_required
# def post_like(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
    
#     #좋아요 취소
#     if request.user in post.like_user_set.all():
#         post.like_user_set.remove(request.user)
#     else:
#         post.like_user_set.add(request.user)
    
#     if request.GET.get('redirect_to') == 'show':
#         return redirect('posts:show', post_id)
#     else:
#         return redirect('posts:main')



@login_required
def like_list(request):
    # likes = Like.objects.filter(user=request.user)
    likes = request.user.like_set.all()
    return render(request,'posts/like_list.html',{'likes':likes})
