from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

from .forms import CommentForm, PostForm
from .models import Post, Category, Comment, User
from .services import (
    create_paginator, filter_published_posts, get_post_annotation,
)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    posts = category.posts.all()
    filtered_posts = filter_published_posts(get_post_annotation(posts))
    page_obj = create_paginator(filtered_posts, request)
    return render(
        request,
        'blog/category.html',
        {'category': category, 'page_obj': page_obj}
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        post = get_object_or_404(
            filter_published_posts(Post.objects.all()),
            pk=post_id
        )
    comments = post.comments.all().order_by('created_at')
    page_obj = create_paginator(comments, request)
    return render(
        request,
        'blog/detail.html',
        context={
            'post': post,
            'page_obj': page_obj,
            'form': CommentForm()
        }
    )


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all()
    annotated_posts = get_post_annotation(posts)
    if request.user != profile_user:
        filtered_posts = filter_published_posts(annotated_posts)
    else:
        filtered_posts = annotated_posts
    page_obj = create_paginator(filtered_posts, request)
    return render(
        request,
        'blog/profile.html',
        {'page_obj': page_obj, 'profile': profile_user, 'posts': posts}
    )


def index(request):
    posts = Post.objects.all()
    filtered_posts = filter_published_posts(get_post_annotation(posts))
    page_obj = create_paginator(filtered_posts, request)
    return render(
        request,
        'blog/index.html',
        {'page_obj': page_obj}
    )


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_published=True)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author:
        return redirect('blog:post_detail', post_id=post_id)

    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)

    return render(
        request,
        'blog/comment.html',
        {
            'form': form,
            'comment': comment,
            'post_id': post_id,
            'comment_id': comment_id
        }
    )


@login_required
def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(
        request,
        'blog/comment.html',
        context={'comment': comment}
    )


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        create_post = form.save(commit=False)
        create_post.author = request.user
        create_post.save()
        return redirect('blog:profile', username=request.user.username)

    return render(
        request,
        'blog/create.html',
        context={'form': form}
    )


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post_id)

    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)

    return render(
        request,
        'blog/create.html',
        context={'form': form, 'post': post, 'is_edit': True}
    )


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog:profile', username=request.user.username)

    form = PostForm(instance=post)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)
    return render(
        request,
        'blog/create.html',
        context={'form': form}
    )
