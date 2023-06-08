from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm, FilterForm
from .filters import ListingFilter


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
    posts = Post.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=posts)
    filtered_posts = listing_filter.qs  # Get the filtered queryset from ListingFilter
    context = {
        'posts': filtered_posts,  # Use the filtered_posts instead of all_posts #posts,
        'listing_filter': listing_filter
    }
    return render(request, 'postsvenues.html', context)


#def venue(request, pk):
 #   venue = Post.objects.filter(pk=pk)
  #  context = {'venue': venue}
   # return render(request, 'venue.html', context)

#is_valid_queryparam gehört zu filter_list


def is_valid_queryparam(param):
    return param != '' and param is not None


def filter_list(request):
    qs = Post.objects.all()
    #location_type = Post.category
    city = Post.city_choices
    max_guest = Post.max_guest

    title_contains_query = request.GET.get('title_contains')
    city_query = request.GET.get('city')
    max_guest_query = request.GET.get('max_guest')

    # Title
    if title_contains_query != '' and title_contains_query is not None:
        qs = qs.filter(title__icontains=title_contains_query)

    # city
    if is_valid_queryparam(city_query) and city_query != 'Choose...':
        qs = qs.filter(city__iexact=city_query)

    # max_guest
    if is_valid_queryparam(max_guest_query) and max_guest_query != 'Choose...':
        qs = qs.filter(max_guest__iexact=max_guest_query)

    context = {
        'queryset': qs,
        #'location_type': location_type,
        'city': city,
        'max_guest': max_guest,
    }

    return render(request, 'postsvenues.html', context)


class FilterView(TemplateView):
    template_name = 'kismet/postsvenues.html'

    def filter(self, request):  # get request
        form = FilterForm(request.GET)
        form.save()
        posts = Post.objects.all()
        #title_contains = request.GET.get('title_contains')
        filtered = ListingFilter(request.GET, queryset=posts)
        filtered_posts = filtered.qs

        return render(request, self.template_name, filtered_posts)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description', 'city', 'adress', 'min_price', 'max_price', 'max_guest']

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
    fields = ['title', 'description', 'city', 'adress', 'min_price', 'max_price', 'max_guest']

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
