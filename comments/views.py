from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from blog.models import Post
from .forms import CommentForm

@login_required
def add_comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added! Awaiting approval.')
    return redirect('blog_detail', slug=post_slug)
