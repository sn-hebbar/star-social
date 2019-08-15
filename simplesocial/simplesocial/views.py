from django.views.generic import TemplateView
from posts import models
from braces.views import SelectRelatedMixin
from django.views import generic


class HomePage(TemplateView):
    template_name='index.html'
class TestPage(TemplateView):
    template_name='test.html'
class ThanksPage(TemplateView):
    template_name='thanks.html'
class PostList(SelectRelatedMixin,generic.ListView):
    model=models.Post
    select_related=('user','group')
    template_name='home.html'
