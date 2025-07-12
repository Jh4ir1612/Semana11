from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Category
from .forms import PostForm


# Vistas basadas en funciones
def post_list(request):
    posts = Post.objects.all().order_by('-published')
    paginator = Paginator(posts, 5)  # 5 posts por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post/list.html', {'page_obj': page_obj})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        published__year=year,
        published__month=month,
        published__day=day,
        slug=slug
    )
    return render(request, 'blog/post/detail.html', {'post': post})


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = category.get_posts.all()
    return render(request, 'blog/category/detail.html', {
        'category': category,
        'posts': posts
    })


# Vistas basadas en clases
class PostListView(ListView):
    model = Post
    template_name = 'blog/post/list.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-published']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        return queryset


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'
    context_object_name = 'post'


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post/form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post/form.html'
    success_url = reverse_lazy('blog:post_list')


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post/confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')