from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from .forms import UserCreationMultiForm, ProfileForm, ProfileUpdateForm
from .models import Profile

def signup(request):
    if request.method == 'POST':
        if request.POST['user-password1'] == request.POST['user-password2']:
            form = UserCreationMultiForm(request.POST, request.FILES)
            if form.is_valid(): 
                user = form['user'].save()
                profile = form['profile'].save(commit=False)
                profile.user = user
                profile.nick = user
                profile.save()
                auth.login(request, user)
                return redirect('index')
            else:
                user = request.POST['user-username']
                user = User.objects.get(username=user)
                messages.info(request, '아이디가 중복됩니다.')
                return render(request, 'adduser.html')
        else:
            messages.info(request, '비밀번호가 다릅니다.')
            return render(request, 'adduser.html')
    return render(request, 'adduser.html')



class Loginviews(LoginView):
    template_name = 'login.html'
login = Loginviews.as_view()


class LogoutViews(LogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL
logout = LogoutViews.as_view()

@login_required
def userinfo(request):
    conn_user = request.user
    conn_profile = Profile.objects.get(user=conn_user)

    if not conn_profile.profile_image:
        pic_url = ""
    else:
        pic_url = conn_profile.profile_image.url
            
    context = {
        'id' : conn_user.username,
        'nick' : conn_profile.nick,
        'profile_pic' : pic_url,
        'intro' : conn_profile.intro,
    }

    return render(request, 'mypage.html', context=context)

@login_required
def user_select_info(request, writer):
    select_profile = Profile.objects.get(nick=writer)
    select_user = select_profile.user

    if not select_profile.profile_image:
        pic_url = ""
    else:
        pic_url = select_profile.profile_image.url
            
    context = {
        'id' : select_user.username,
        'nick' : select_profile.nick,
        'profile_pic' : pic_url,
        'intro' : select_profile.intro
    }

    return render(request, 'userpage.html', context=context)

class ProfileUpdateView(View): 
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk) 


        if hasattr(user, 'profile'):  
            profile = user.profile
            profile_form = ProfileUpdateForm(initial={
                'nick': profile.nick,
                'intro': profile.intro,
                'profile_image': profile.profile_image,
            })
        else:
            profile_form = ProfileUpdateForm()

        return render(request, 'profile_update.html', { "profile_form": profile_form})

    def post(self, request):
        u = User.objects.get(id=request.user.pk)       


        if hasattr(u, 'profile'):
            profile = u.profile
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile) 
        else:
            profile_form = ProfileUpdateForm(request.POST, request.FILES)

        # Profile 폼
        if profile_form.is_valid():
            profile = profile_form.save(commit=False) 
            profile.user = u
            profile.save()

            if not profile.profile_image:
                pic_url = ""
            else:
                pic_url = profile.profile_image.url
                    
            context = {
                'id' : u.username,
                'nick' : profile.nick,
                'profile_pic' : pic_url,
                'intro' : profile.intro,
            }

            return render(request, 'mypage.html', context=context)
            
        return redirect('mypage', pk=request.user.pk) 