from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ProfileForm, UserUpdateForm
from .models import Profile
from django.contrib import messages


def register(request):
	form = RegisterForm()

	if request.method == "POST":
		form = RegisterForm(request.POST)

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
def profile_page(request):
	# profile = Profile.objects.get(id=request.user.id)
	profile = get_object_or_404(Profile, user_id=request.user.id)
	# profile_update = get_object_or_404(UserUpdateForm, user_id=request.user.id)
	id_ = request.user.id
	user_profile = get_object_or_404(Profile, id=id_)
	form = ProfileForm(instance=user_profile)
	update_form = UserUpdateForm(instance=user_profile)

	if request.method == "POST":
		form = ProfileForm(request.POST, instance=user_profile)
		if form.is_valid() and update_form.is_valid():
			form.save()
			update_form.save()

			if request.FILES.get('image', None) != None:
				print(request.FILES)
				user_profile.image = request.FILES['image']
				user_profile.save()
				messages.success(request, 'Profile was updated successfully!')
			return redirect('profile_page')
	context = {
		'profile': profile,
		'form': form,
		'update_form': update_form
		}

	return render(request, "users/profile.html", context)


def profile_update(request):
	id_ = request.user.id
	user_profile = get_object_or_404(Profile, id=id_)
	form = ProfileForm(instance=user_profile)

	if request.method == "POST":
		form = ProfileForm(request.POST, instance=user_profile)
		if form.is_valid():
			form.save()

			if request.FILES.get('image', None) != None:
				# print(request.FILES)
				user_profile.image = request.FILES['image']
				user_profile.save()
				# messages.success(request, 'Profile was updated successfully!')
			return redirect('profile_page')

	# messages.warning(request, 'Profile was not updated successfully!')
	return render(request, "users/profile_update.html", {'form': form})


@login_required
def logout(request):
	return render(request, 'users/logout.html')

