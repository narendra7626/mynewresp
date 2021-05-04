from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.views.generic import View,ListView,DetailView,CreateView,TemplateView,UpdateView,DeleteView
from myapp.forms import *
from myapp.models import *
from django.contrib.auth.models import User

from django.urls import reverse,reverse_lazy
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework import viewsets
from myapp.serializers import PostSerializer,CommentSerializer
from rest_framework import mixins
from django.contrib import messages
# Create your views here.
def index(request):
    post_list=Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')
    paginator=Paginator(post_list,5)
    page_number=request.GET.get('page')
    post_obj=paginator.get_page(page_number)
    data=Category.objects.all()
    return render(request,'myapp/post_list.html',{'post_list':post_obj,'data':data})

class DraftListView(LoginRequiredMixin,ListView):
    form_class=PostForm
    model=Post
    login_url='/login/'
    def get_queryset(self):
        return Post.objects.filter(publish_date__isnull=True).order_by('create_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = Post.objects.all()
        context['data'] = data
        return context


def signupview(request):
    data = Category.objects.all()
    if request.method=="POST":
        form1=SignupForm(request.POST,request.FILES)
        form2=UserProfileForm(request.POST,request.FILES)
        username=request.POST.get('username')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        gender=request.POST.get('gender')
        image=request.FILES.get('image')
        if(len(first_name)==0 and len(last_name) == 0 and len(email) == 0):
            messages.success(request, 'Please Enter All Details')
        else:
            if form1.is_valid() and form2.is_valid():
                user=form1.save()
                profile=form2.save(commit=False)
                profile.user=user
                profile.save()
                messages.success(request,'User Registered Successfully')
                return redirect('register')
            else:
                if User.objects.filter(username=username).exists():
                    messages.success(request,'Username Already Taken')
                elif(password1!=password2):
                    messages.success(request,'Password Did not Match')

                else:
                    messages.success(request,'Error while registering')





    else:
        form1=SignupForm()
        form2=UserProfileForm()

    return render(request,'register/registration.html',{'data':data})





def user_login(request):
    data=Category.objects.all()
    if request.method=='POST':
        request.session['username']=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=request.session['username'],password=password)
        if len(request.session['username'])==0:
            messages.success(request,"Please Enter Username")
        elif len(password)==0:
            messages.success(request,'Please enter Password')
        else:
            if user:
                if request.session.has_key('username'):

                    login(request,user)
                    return redirect('index')
                else:
                    messages.success(request,"invlaid")
            else:
                messages.success(request,"Invalid Credentials")
                return redirect('login')
    return render(request,'register/login.html',{'data':data})



@login_required
def user_logout(request):
    try:
        logout(request)
        del request.session['username']
    except:
        pass
    return HttpResponseRedirect(reverse('index'))


class PostCreateView(LoginRequiredMixin,CreateView):
    login_url='/login/'
    form_class=PostForm
    model=Post
    success_url=reverse_lazy('index')

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        data=Category.objects.all()
        context['data']=data
        return context

class PostDetailView(DetailView):
    model=Post

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        data=Category.objects.all()
        context['data']=data
        return context

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    model=Post
    form_class=PostForm
    success_url=reverse_lazy('index')

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['data']=Category.objects.all()
        return context

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post
    form_class=PostForm
    success_url=reverse_lazy('index')

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        data=Category.objects.all()
        context['data']=data
        return context

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def add_comment_post(request,pk):
    data=Category.objects.all()
    post=get_object_or_404(Post,pk=pk)
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form=CommentForm()
    return render(request,'myapp/comment_form.html',{'form':form,'post':post,'data':data})

@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)
@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.delete()
    post_pk=comment.post.pk
    return redirect('post_detail',pk=post_pk)

def search(request):
    data=Category.objects.all()
    if 'q' in request.GET:
        q=request.GET['q']
        posts=Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')
        post_list=posts.filter(title__icontains=q)
    else:
        post_list=Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')
    return render(request,'myapp/search.html',{'post_list':post_list,'data':data})


def cat_post(request,cat_id):
    category=Category.objects.get(id=cat_id)
    posts=Post.objects.filter(category=category)
    data=Category.objects.all()
    return render(request,'myapp/cat_post.html',{'category':category,'data':data,'posts':posts})


class PostViewset(viewsets.ModelViewSet):
    serializer_class=PostSerializer
    queryset=Post.objects.all()

class CommentViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class=CommentSerializer
    queryset=Comment.objects.all()




