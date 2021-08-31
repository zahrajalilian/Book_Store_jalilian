from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# eationForm
from django.shortcuts import render

# Create your views here.
# from django.urls import reverse_lazy
# from django.views.generic import CreateView

# from accounts.forms import CustomUserCreationForm

#
# class SignUpView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/signup.html'
#
# def signup(request):
#     if request.method == 'POST':
#         pass
#     else:
#
#     return render(request,'accounts/signup.html')

# /////////////////////////////////////////////////////////////////
from django.views.generic import UpdateView

from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from .decorators import allowed_users,admin_only,unauthenticated_user
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

@unauthenticated_user
def user_register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # clean
            data = form.cleaned_data
            group = Group.objects.get(name='customer')
            user = CustomUser.objects.create_user(username=data['username'], email=data['email'],
                                     first_name=data['first_name'],
                                     last_name=data['last_name'],
                                     password=data['password2'])

            user.groups.add(group)
            user.save()
            messages.success(request, 'account created for',user)
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'register.html', context )


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = authenticate(request, username=CustomUser.objects.get(email=data['user']),
                                    password=data['password'])
            except:
                user = authenticate(request, username=data['user'], password=data['password'])

            if user is not None:
                login(request, user)
                messages.success(request, 'به فروشگاه کتاب  خوش آمدید', 'primary')
                return redirect('home')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور شتباه است', 'danger')

    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form':form})



def user_logout(request):
    logout(request)
    messages.success(request,'با موفقیت خارج شدید', 'warning')
    return redirect('home')
# //////////////////////////////////////////////////

@login_required(login_url='login')
def user_profile(request):
    profile = Profile.objects.get(user_id = request.user.id)
    return render(request, 'profile.html', {'profile':profile})

#
# @login_required(login_url='login')
# def user_update(request):
#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=request.user)
#         profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
#         if user_form and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'update successfully', 'success')
#             return redirect('profile')
#     else:
#         user_form =UserUpdateForm(instance=request.user)
#         profile_form = ProfileUpdateForm(instance=request.user.profile)
#     context = {'user_form': user_form, 'profile_form':profile_form}
#     return render(request,'update.html', context)


class UpdateProfile(UpdateView):
    # permission_required = 'book.change_Book'
    # permission_denied_message = ' sorry cant access to this page'
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'update.html'
    fields = ['address', 'fax', 'phone', 'company']
