from django.db import models
from django.db.models import Count
from django.utils.timezone import now
from django.core.paginator import Paginator
from .constants import POSTS_PER_PAGE


class PostQuerySet(models.QuerySet):
    def get_filtered_posts(self):
        return self.filter(
            pub_date__lte=now(),
            is_published=True,
            category__is_published=True
        ).select_related('author', 'location', 'category').order_by('-pub_date')


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)


class CommentQuerySet(models.QuerySet):
    def annotate_total_comments(self):
        return self.annotate(total_comments=Count('id'))


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)


def paginate_posts(posts, page_number):
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_obj = paginator.get_page(page_number)
    return page_obj
