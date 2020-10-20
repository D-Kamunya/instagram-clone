from django.shortcuts import render,redirect
from django.http  import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .models import Image,Like
from .forms import NewImageForm
from users import views as user_views
# Create your views here.

def get_liked_posts(request):
  liked_posts=Like.objects.filter(user=request.user)
  return liked_posts


@login_required(login_url='/accounts/login/')
def home_page(request):
  following=user_views.get_following(request)
  following_posts=[]
  all_posts=Image.get_all_images()
  for post in all_posts:
    if post.profile in following:
      following_posts.append(post)
  profile=Profile.get_profile_by_userid(request.user.id)
  my_posts=Image.filter_by_userid(request.user.id)
  context={
    'profile':profile,
    'following':following,
    'all_posts':all_posts,
    'following_posts':following_posts,
    'my_posts':my_posts
  }
  return render(request,'feed/home.html',context)



@login_required(login_url='/accounts/login/')
def new_post(request):
    current_profile = request.user.profile
    if request.method == 'POST':
        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = current_profile
            image.save()
        return redirect('home_page')

    else:
        form = NewImageForm()
    context={
      'profile':current_profile,
      'form':form
    }    
    return render(request, 'feed/new_image.html',context)



@login_required(login_url='/accounts/login/')
def post(request,post_id):
  post=Image.get_image_by_id(post_id)
  posts_liked=[]
  for like in get_liked_posts(request):
    posts_liked.append(like.post)
  print(posts_liked) 
  print(post)  
  context={
    'profile':request.user.profile,
    'post':post,
    'posts_liked':posts_liked

  }
  return render(request, 'feed/post.html',context)



@login_required(login_url='/accounts/login/')
def like_post(request,post_id):
  post=Image.get_image_by_id(post_id)
  user=request.user
  like = Like.objects.filter(user=user, post=post)
  if like:
    like.delete()
  else:
    Like.objects.create(user=user,post=post)  

  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

