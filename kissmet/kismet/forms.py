from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import Post
import django_filters


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = Post
        fields = ('title', 'description', 'city', 'adress', 'min_price', 'max_price', 'max_guest')


class FilterForm(forms.Form):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    city = django_filters.ChoiceFilter(choices=Post.city_choices)
    #location_type = django_filters.ChoiceFilter(choices=Post.location_style_choices)
    max_guest = django_filters.ChoiceFilter(choices=Post.max_guest)
