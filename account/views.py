from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from common.decorators import ajax_required
from actions.utils import create_action


User = get_user_model()


@login_required
def dashboard(request):
    context = {
        'section': dashboard,
    }
    return render(request, 'account/dashboard.html', context)



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
            user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            Profile.objects.create(user=new_user)
            create_action(request.user, 'has created an account')
            context = {
                'new_user': new_user
            }
            return render(request, 'account/register_done.html', context)

    user_form = UserRegistrationForm()
    context = {
        'user_form': user_form
    }
    return render(request, 'account/register.html', context)



@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
            data=request.POST,
            files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating you profile')

    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'account/edit.html', context)



@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    context = {
        'section': 'people',
        'users': users,
    }
    return render(request, 'account/user/list.html', context)



@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)

    context = {
        'section': 'people',
        'user': user,
    }
    return render(request, 'account/user/detail.html', context)



@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')

    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                    user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                    user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})
