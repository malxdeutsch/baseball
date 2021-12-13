from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import 
from django.views.generic import CreateView
import random

class CommentCreateView(CreateView):
    model = Comment
    fields = ['content', 'phone_number']
    template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(id=self.kwargs['post_id'])
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=post_id)
        self.object.post = post
        self.object.save()
        return super().form_valid(form)
    
def my_posts(request):
    return render(request,'posts/my_posts.html')


def post_create(request):
    form = PostModelForm()
    if request.method == "POST":

        form = PostModelForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.likes = 0
            post.save()
            # EITHER THIS
            response_dict = {
                'title': post.title,
                'owner': post.owner.username,
                'content': post.content,
            }
            # OR THIS
            instance_dict = model_to_dict(post, fields=['title', 'content'])
            instance_dict['owner'] = post.owner.username


            return JsonResponse(response_dict, status=201)
        else:
            return JsonResponse(form.errors, safe=False, status=400)

    return render(request, 'posts/post_fetch_form.html', {'form': form, 'posts': Post.objects.all()})