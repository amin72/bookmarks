from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm


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
            context = {
                'new_user': new_user
            }
            return render(request, 'account/register_done.html', context)

    user_form = UserRegistrationForm()
    context = {
        'user_form': user_form
    }
    return render(request, 'account/register.html', context)
