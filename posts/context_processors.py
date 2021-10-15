from posts.models import Post
from taggit.models import Tag


def list_tags(request):
    """
    List tags belong to the user (sidebar)
    # """
    if request.user.is_authenticated:
        posts_id = Post.objects.filter(user=request.user).values_list('tags', flat=True)
        tags = Tag.objects.filter(id__in=posts_id)
    else:
        tags = ""
    return {"tags": tags}
