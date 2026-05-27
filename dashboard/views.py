from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from blog.models import Post, Category, Tag
from comments.models import Comment
from blog.forms import PostForm
from django import forms

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

def admin_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('dashboard_login')
        if not request.user.is_staff and not request.user.is_superuser:
            messages.error(request, 'Access denied.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def login_view(request):
    from django.contrib.auth import login, authenticate
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and (user.is_staff or user.is_superuser):
            login(request, user)
            return redirect('dashboard_home')
        else:
            messages.error(request, 'Invalid credentials or not a staff user.')
    return render(request, 'dashboard/login.html')

@admin_login_required
def home(request):
    total_posts = Post.objects.count()
    published_posts = Post.objects.filter(status='published').count()
    draft_posts = Post.objects.filter(status='draft').count()
    total_categories = Category.objects.count()
    total_users = User.objects.count()
    total_comments = Comment.objects.count()
    recent_posts = Post.objects.order_by('-created_at')[:5]
    context = {
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'total_categories': total_categories,
        'total_users': total_users,
        'total_comments': total_comments,
        'recent_posts': recent_posts,
    }
    return render(request, 'dashboard/index.html', context)

@admin_login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'dashboard/posts.html', {'posts': posts})

@admin_login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Post created!')
            return redirect('dashboard_posts')
    else:
        form = PostForm()
    return render(request, 'dashboard/post_form.html', {'form': form, 'edit': False})

@admin_login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated!')
            return redirect('dashboard_posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'dashboard/post_form.html', {'form': form, 'edit': True})

@admin_login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.success(request, 'Post deleted!')
    return redirect('dashboard_posts')

@admin_login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/categories.html', {'categories': categories})

@admin_login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created!')
            return redirect('dashboard_categories')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category_form.html', {'form': form, 'edit': False})

@admin_login_required
def category_edit(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated!')
            return redirect('dashboard_categories')
    else:
        form = CategoryForm(instance=cat)
    return render(request, 'dashboard/category_form.html', {'form': form, 'edit': True})

@admin_login_required
def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    cat.delete()
    messages.success(request, 'Category deleted!')
    return redirect('dashboard_categories')

@admin_login_required
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'dashboard/tags.html', {'tags': tags})

@admin_login_required
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag created!')
            return redirect('dashboard_tags')
    else:
        form = TagForm()
    return render(request, 'dashboard/tag_form.html', {'form': form, 'edit': False})

@admin_login_required
def tag_edit(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag updated!')
            return redirect('dashboard_tags')
    else:
        form = TagForm(instance=tag)
    return render(request, 'dashboard/tag_form.html', {'form': form, 'edit': True})

@admin_login_required
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    messages.success(request, 'Tag deleted!')
    return redirect('dashboard_tags')

@admin_login_required
def comment_list(request):
    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'dashboard/comments.html', {'comments': comments})

@admin_login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approved = True
    comment.save()
    messages.success(request, 'Comment approved!')
    return redirect('dashboard_comments')

@admin_login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    messages.success(request, 'Comment deleted!')
    return redirect('dashboard_comments')

@admin_login_required
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/users.html', {'users': users})
