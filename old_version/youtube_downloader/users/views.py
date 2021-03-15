from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
# from .forms import RegisterForm, ProfileForm, UserUpdateForm, ProfileUpdateForm
from .forms import ProfileUpdateForm, UserUpdateForm, UserRegisterForm
from .models import Profile
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse


def register(request):
    form = UserRegisterForm()

    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'User was created successfully!')
            username = form.data.get("username")
            password = form.data.get("password1")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
            return redirect("home_page")

    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.add_message(request, messages.SUCCESS, "Your account has been updated!")
            return redirect('profile_page')

    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
                'u_form': u_form,
                'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


# @login_required
# def profile(request):
#
#     user_profile = get_object_or_404(Profile, user_id=request.user.id)
#
#     context = {
#                 "profile": user_profile
#     }
#     return render(request, 'users/profile.html', context)


@login_required
def logout(request):
    return render(request, 'users/logout.html')
