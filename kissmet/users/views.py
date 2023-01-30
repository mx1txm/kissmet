from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserProfileForm, UserUpdateForm, ProfileUpdateForm, ProfileDeleteForm, UserDeleteForm
from django.contrib.auth.models import User


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        p_form = UserProfileForm(request.POST)
        if form.is_valid() and p_form. is_valid():
            user = form.save()
            profile = p_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login')
            return redirect('login')
    else:
            form = UserRegisterForm()
            p_form = UserProfileForm()

    context = {
        'form': form,
        'p_form': p_form
    }
    return render(request, 'users/register.html', context)

def list_all(request):
    context = {
        'users': User.objects.all
    }
    return render(request, 'users/list_all.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form. is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    elif request.method == 'DELETE':
        return redirect('kismet-home')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


@login_required
def deleteuser(request):
    if request.method == 'POST':
        delete_form = UserDeleteForm(request.POST, instance=request.user)
        user = request.user
        user.delete()
        messages.info(request, 'Your account has been deleted.')
        return redirect('kismet-home')
    else:
        delete_form = UserDeleteForm(instance=request.user)

    context = {
        'delete_form': delete_form
    }
    return render(request, 'users/profile.html', context)

def profile_confirm_delete(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'users/profile_confirm_delete.html', context)
