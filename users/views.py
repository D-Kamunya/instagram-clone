from django.shortcuts import render,redirect
from django.http  import HttpResponse,HttpResponseRedirect
from .forms import SignUpForm,UserProfileForm,EditProfileForm
from django.contrib.auth import login, authenticate
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from .models import Profile
from feed.models import Image
from django.contrib.auth.models import User
from friendship.models import Friend, Follow,Block 
from django.contrib import messages
# Create your views here.

@login_required(login_url='/accounts/login/')
def new_user(request):
  user_bio=request.user.profile.bio
  user_profile_photo=request.user.profile.bio
  user_posts=Image.filter_by_userid(request.user.id)
  user_following=Follow.objects.following(request.user)
  if (len(user_bio)==0) and (len(user_profile_photo)==0) and (len(user_posts)==0) and (len(user_following)==0):
    return True
  else:
    return False  



@login_required(login_url='/accounts/login/')
def get_not_following(request):
  all_profiles=Profile.get_all_profiles(request.user)
  following=Follow.objects.following(request.user)
  following_id=[]
  for followin in following:
    following_id.append(followin.id)
  not_following=[]
  for profile in all_profiles:
    if profile.user.id not in following_id:
      not_following.append(profile)
  return not_following


@login_required(login_url='/accounts/login/')
def get_following(request):
  all_profiles=Profile.get_all_profiles(request.user)
  following=Follow.objects.following(request.user)
  following_id=[]
  for followin in following:
    following_id.append(followin.id)
  following=[]
  for profile in all_profiles:
    if profile.user.id in following_id:
      following.append(profile)
  return following 

@login_required(login_url='/accounts/login/')
def get_followers(request):
  all_profiles=Profile.get_all_profiles(request.user)
  followers=Follow.objects.followers(request.user)
  followers_id=[]
  for follower in followers:
    followers_id.append(follower.id)
  followers=[]
  for profile in all_profiles:
    if profile.user.id in followers_id:
      followers.append(profile)
  return followers    



def register_user(request):
  if request.method == "POST":
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, f'Account for username {username} successfully created.')
        return redirect('home_page')
  else:
      form = SignUpForm() 
  return render(request, 'registration/registration_form.html', {'form': form})



@login_required(login_url='/accounts/login/')
def not_following(request):
  
  not_following_profiles=get_not_following(request)
  prof=request.user.profile
  context={
    'profile':prof,
    'not_following':not_following_profiles
  }
  return render(request, 'users/not_following.html', context) 


@login_required(login_url='/accounts/login/')
def  add_following(request,follow_id):
  following_user=User.objects.get(pk=follow_id)
  Follow.objects.add_follower(request.user, following_user)
  messages.success(request, f'Started following {Profile.get_profile_by_userid(following_user).user.username} ')
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/accounts/login/')
def remove_following(request,follow_id):
  following_user=User.objects.get(pk=follow_id)
  Follow.objects.remove_follower(request.user, following_user)
  messages.success(request, f'Stopped following {Profile.get_profile_by_userid(following_user).user.username} ')
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/accounts/login/')
def my_profile(request):
  from feed.views import get_likes
  posts_liked=[]
  for like in get_likes(request):
    posts_liked.append(like.post) 
  profile=request.user.profile
  following=get_following(request)
  followers=get_followers(request)
  my_posts=Image.filter_by_userid(request.user.id)
 
  context={
    'profile':profile,
    'following':following,
    'followers':followers,
    'posts':my_posts,
    'posts_liked':posts_liked
  }
  return render(request, 'users/my_profile.html',context)




@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)  # request.FILES is show the selected image or file

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            messages.success(request, f'Profile updated successfully')
            return redirect('my_profile')
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
        context={
          'form':form,
          'profile_form':profile_form,
          'profile':request.user.profile
        }
        return render(request, 'users/edit_profile.html',context)



@login_required(login_url='/accounts/login/')
def search_users(request):

    if 'user_name' in request.GET and request.GET["user_name"]:
        search_term = request.GET.get("user_name")
        users =User.objects.filter(username__icontains=search_term)
        message = f"{search_term}"
        following=get_following(request)
        context={
          "message":message,
          "users": users,
          'profile':request.user.profile,
          'following':following
        }
        return render(request, 'search.html',context)

    else:
        message = "You haven't searched for any user"
        context={
          "message":message,
          'profile':request.user.profile
        }
        return render(request, 'search.html',context)

