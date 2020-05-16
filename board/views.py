from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Board
from .forms import BoardForm

# Create your views here.
def post_list(request):
    posts = Board.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'board/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Board, pk=pk)
    return render(request, 'board/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('board:post_detail', pk=post.pk)
    else:
        form = BoardForm()
    return render(request, 'board/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Board, pk=pk)
    if request.method == "POST":
        form = BoardForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('board:post_detail', pk=post.pk)
    else:
        form = BoardForm(instance=post)
    return render(request, 'board/post_edit.html', {'form': form})