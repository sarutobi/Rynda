# -*- coding: utf-8 -*-

from django.utils import timezone

from rynda.core.views import RyndaListView
from .models import Post


class NewsListView(RyndaListView):
    queryset = Post.objects.filter(
        status=Post.PUBLISHED, publish__lte=timezone.now())
    template_name = "post_list.html"
    context_object_name = "posts"
    paginator_url = "/news/?page="
    paginate_by = 10
