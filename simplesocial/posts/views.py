from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from django.contrib import messages
from braces.views import SelectRelatedMixin
from . import models
from . import forms
from django.contrib.auth.decorators import login_required


from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

class PostList(SelectRelatedMixin,generic.ListView):
    model=models.Post
    select_related=('user','group')

class UserPosts(generic.ListView):
    model=models.Post
    template_name='posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(username__iexact=self.kwargs.get("username"))
        except User.DoesNotExists:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['post_user']=self.post_user
        return context

class PostDetail(SelectRelatedMixin,generic.DetailView):
    model=models.Post
    select_related=('user','group')

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['form'] = forms.CommentForm
        return context


class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    fields = ('message','group','image')
    model = models.Post
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model=models.Post
    select_related=('user','group')
    success_url=reverse_lazy('posts:all')

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)

"""@login_required(login_url='/accounts/login/')
def add_comment_to_post(request,pk):
    post=get_object_or_404(models.Post,pk=pk)
    user = request.user
    #user=get_object_or_404(User,username=self.username)
    if request.method=="POST":
        form=forms.CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.comment_writer=user
            comment.save()
            return redirect('posts:single',pk=post.pk,username=post.user.username)

    else:
        form=forms.CommentForm()
    return render(request,'posts/comment_form.html',{'form':form})"""

class AddComment(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    fields = ('text',)
    model = models.Comment
    def form_valid(self, form):
        pk=self.kwargs['pk']
        post=models.Post.objects.get(pk=pk)
        self.object = form.save(commit=False)
        self.object.comment_writer = self.request.user
        self.object.post=post
        self.object.save()
        return super().form_valid(form)
