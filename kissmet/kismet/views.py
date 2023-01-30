from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm


def home(request):
    return render(request, 'home.html', {})


def newpost(request):

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = PostForm()
    return render(request, 'newpost.html', {'form': form})


def postsvenues(request):
    context = {
        'posts': Post.objects.all() #all
    }
    return render(request, 'postsvenues.html', context)


def venue(request, pk):
    venue = Post.objects.filter(pk=pk)
    context = {'venue': venue}
    return render(request, 'venue.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['Titel', 'Beschreibung', 'Stadt', 'Adresse', 'Mindestpreis', 'Hoechstpreis', 'maxGaesteanzahl']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    template_name = 'kismet/postsvenues.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']  # ordering posts from latest to oldest

    def get_queryset(self):
        qs = self.model.objects.all()
        print(qs)

        return render(self.template_name, qs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'venue.html'

    def postdetail(request):
        posts = Post.objects.get(pk=request.GET.get('value'))
        return render(request, 'post/<int:pk>/', {'item': posts})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['Titel', 'Beschreibung', 'Stadt', 'Adresse', 'Mindestpreis', 'Hoechstpreis', 'maxGaesteanzahl']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):  # prevent that a user can update other users posts
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):  # prevent that a user can update other users posts
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
