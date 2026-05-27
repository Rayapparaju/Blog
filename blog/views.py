from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Post, Category

def home(request):
    featured_posts = Post.objects.filter(status='published', featured=True)[:3]
    latest_posts = Post.objects.filter(status='published')[:6]
    categories = Category.objects.all()
    context = {
        'featured_posts': featured_posts,
        'latest_posts': latest_posts,
        'categories': categories,
    }
    return render(request, 'home.html', context)

def blog_list(request):
    posts = Post.objects.filter(status='published')
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'categories': categories,
        'current_category': category_slug,
    }
    return render(request, 'blog_list.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.filter(category=post.category, status='published').exclude(id=post.id)[:3]
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog_detail.html', context)

def search(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(
        Q(status='published'),
        Q(title__icontains=query) | Q(content__icontains=query) | Q(excerpt__icontains=query)
    ) if query else Post.objects.none()
    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'search_results.html', context)
