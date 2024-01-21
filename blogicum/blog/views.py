from django.utils import timezone
from django.shortcuts import get_object_or_404, render

from .models import Category, Post

POSTS_MAX = 5


def posts():
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )


def index(request):
    return render(request, 'blog/index.html',
                  {'post_list': posts()[:POSTS_MAX]})


def post_detail(request, id):
    post = get_object_or_404(posts(), id=id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    context = {'category': category,
               'post_list': posts().filter(category=category)}
    return render(request, 'blog/category.html', context)
