from django.core.paginator import Paginator
from django.db.models import Count
from django.utils.timezone import now

from .constants import POSTS_PER_PAGE


def create_paginator(posts, request):
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def get_post_annotation(posts_queryset):
    return posts_queryset.annotate(
        comment_count=Count('comments')).select_related(
        'author', 'location', 'category'
    ).order_by('-pub_date')


def filter_published_posts(posts_queryset):
    return posts_queryset.filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True
    )
