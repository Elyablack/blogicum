from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.timezone import now

from .forms import CommentForm, PostForm
from .models import Post, Category, Comment, User
from .service import paginate_posts


def index(request):
    posts = Post.objects.get_queryset().get_filtered_posts()
    page_obj = paginate_posts(posts, request.GET.get('page'))
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = category.posts.get_filtered_posts()
    page_obj = paginate_posts(posts, request.GET.get('page'))
    return render(
        request,
        'blog/category.html',
        {'category': category, 'page_obj': page_obj}
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        post = Post.objects.get_queryset().get(pk=post_id)
    comments_queryset = post.comments.all()
    comments = comments_queryset.annotate_total_comments()
    form = CommentForm()
    return render(
        request,
        'blog/detail.html',
        context={
            'post': post,
            'comments': comments,
            'requser': request.user,
            'form': form
        })


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.get_queryset().filter(
        author=profile_user).get_filtered_posts()
    page_obj = paginate_posts(posts, request.GET.get('page'))
    return render(
        request,
        'blog/profile.html',
        {'page_obj': page_obj, 'profile': profile_user, 'posts': posts}
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
    if request.user == comment.author:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('blog:post_detail', post_id=post_id)
        else:
            form = CommentForm(instance=comment)
        return render(
            request,
            'blog/comment.html',
            {
                'form': form,
                'comment': comment,
                'post_id': post_id,
                'comment_id': comment_id
            })
    else:
        return redirect('blog:post_detail', post_id=post_id)


@login_required
def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    context = {'comment': comment}
    return render(
        request,
        'blog/comment.html',
        context=context
    )


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None)
    if form.is_valid():
        create_post = form.save(commit=False)
        create_post.author = request.user
        create_post.pub_date = now()

        if create_post.pub_date > now():
            create_post.is_published = False
        else:
            create_post.is_published = True

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

    form = PostForm(request.POST or None,
                    request.FILES or None,
                    instance=post)

    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)

    template = 'blog/create.html'
    context = {'form': form, 'post': post, 'is_edit': True}
    return render(request, template, context)


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('blog:profile', username=request.user.username)
