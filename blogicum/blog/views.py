from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now

from .models import Post, Category
from .constants import POSTS_PER_PAGE


def get_filtered_posts(post_manager):
    return post_manager.filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True
    ).select_related('author', 'location', 'category')


def index(request):
    posts = get_filtered_posts(Post.objects)[:POSTS_PER_PAGE]
    return render(request, 'blog/index.html', {'posts': posts})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = get_filtered_posts(category.posts.all())
    return render(
        request,
        'blog/category.html',
        {'category': category, 'posts': posts}
    )


def post_detail(request, post_id):
    post_manager = Post.objects
    post = get_object_or_404(
        get_filtered_posts(post_manager),
        pk=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})
