from django.shortcuts import render, get_object_or_404, Http404
from django.views.generic import (DetailView, UpdateView,
                                  DeleteView, CreateView,
                                  ListView, View)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from django.core.paginator import Paginator
from django.db.models import Q
import operator
from functools import reduce
from mixins import OwnerMixin, HeaderWizard
from .models import Post
from .forms import PostForm, DateForm


class PostDetail(LoginRequiredMixin, OwnerMixin, DetailView):
    model = Post


class ListPost(LoginRequiredMixin, OwnerMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/post_list.html'
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        qs = user.posts.all()
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # for date widget
        context['form'] = DateForm()
        return context


class PostTagSearch(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/post_list.html'
    paginate_by = 5

    def get_queryset(self, **kwargs):
        """
        objects belong to the particular user
        """
        qs = Post.objects.filter(user=self.request.user)
        tag = self.kwargs.get('tag')
        if tag:
            qs = qs.filter(tags__name__in=[tag])
        return qs


class SearchPost(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    flag = False
    not_found = False

    def get_queryset(self, *args, **kwargs):
        words = self.request.GET.get('q')
        if words is not None:
            qs = Post.objects.filter(user=self.request.user)
            query_list = words.split()
            if len(query_list) != 0:
                lookup = qs.filter(
                    reduce(operator.or_,
                           (Q(title__icontains=word) for word in query_list)) |
                    reduce(operator.or_,
                           (Q(content__icontains=word) for word in query_list))
                ).distinct()
                if lookup:
                    return lookup
                else:
                    self.not_found = "Nothing found for this search"
                    return Post.objects.none()
                # user's input == empty string
                self.flag = True
                return Post.objects.none()

        else:
            return Post.objects.none()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.flag:
            context['flag'] = self.flag
        if self.not_found:
            context['not_found'] = self.not_found
        return context


class CreatePost(LoginRequiredMixin, SuccessMessageMixin,
                 HeaderWizard, CreateView):
    form_class = PostForm
    template_name = 'posts/post_form.html'
    header_title = "Create Post"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        form.save_m2m()
        return super().form_valid(form)


class EditPost(LoginRequiredMixin, SuccessMessageMixin,
               HeaderWizard, UpdateView):
    form_class = PostForm
    template_name = 'posts/post_form.html'
    succcess_message = "You've just changed your post"

    def get_object(self, queryset=None):
        unid_ = self.kwargs.get('post_unid')
        obj = get_object_or_404(Post, unid=unid_, user=self.request.user)
        if obj.user != self.request.user:
            raise Http404
        return obj

    def get_success_message(self, *args, **kwargs):
        return self.succcess_message

    def get_header_title(self):
        obj = self.get_object()
        return "Edit post titled as: {}".format(obj.title)


class PostDelete(LoginRequiredMixin, OwnerMixin, SuccessMessageMixin, DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('posts:all-posts')
    succcess_message = "You've just deleted your post"

    def get_success_message(self, *args, **kwargs):
        return self.succcess_message


class ManualFormView(LoginRequiredMixin, View):
    def post(self, request):
        form = DateForm(request.POST)
        if form.is_valid():
            date = request.POST.get('date')
            post_list = Post.objects.filter(user=request.user, created=date)
            paginator = Paginator(post_list, 25)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {'posts': post_list, 'page_obj': page_obj}
            return render(request, 'posts/post_list.html', context)
        else:
            context = {'arch_form': form, 'err': 'Enter a valid date please'}
            # 'waarde van ‘02/03/2020’ heeft een ongeldige datumnotatie. De juiste notatie is YYYY-MM-DD.'
            return render(request, 'posts/post_list.html', context)
