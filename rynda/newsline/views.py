# -*- coding: utf-8 -*-

import datetime

from core.views import RyndaListView

from .models import Post


class NewsListView(RyndaListView):
    queryset = Post.objects.filter(
        status=Post.PUBLISHED, publish__lte=datetime.datetime.now())
    template_name = "latest_post.html"
    context_object_name = "posts"
    paginator_url = "/news/?page="
    paginate_by = 10
