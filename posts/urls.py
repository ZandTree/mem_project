from django.urls import path, re_path
from .views import (PostDetail, CreatePost, EditPost, ListPost,
                    SearchPost, PostDelete, PostTagSearch,
                    ManualFormView)

app_name = "posts"

urlpatterns = [

    path('delete-post/<post_unid>/', PostDelete.as_view(), name='post-delete'),
    path('all-posts/', ListPost.as_view(), name="all-posts"),
    path('create/', CreatePost.as_view(), name="post-create"),
    path('detail/<post_unid>/', PostDetail.as_view(), name="post"),
    path('edit/<post_unid>/', EditPost.as_view(), name="post-edit"),
    path('search-post/', SearchPost.as_view(), name="search"),
    re_path(r'^tag-search/(?:t:(?P<tag>[-\w]+)/)?$', PostTagSearch.as_view(), name="tag-search"),
    path('arch-form/', ManualFormView.as_view(), name='arch'),

]
