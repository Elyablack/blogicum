from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now

from .models import Post, Category
from .constants import POSTS_PER_PAGE


def get_filtered_posts(post_manager):
    return post_manager.filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True
    ).select_related('author', 'location', 'category').order_by('id')


def index(request):
    posts = get_filtered_posts(Post.objects)
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})

def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = get_filtered_posts(category.posts.all())
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'blog/category.html',
        {'category': category, 'page_obj': page_obj}
    )


def post_detail(request, post_id):
    post_manager = Post.objects
    post = get_object_or_404(
        get_filtered_posts(post_manager),
        pk=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user, is_published=True)
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'blog/profile.html',
        {'page_obj': page_obj, 'profile': profile_user}
    )