import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm

logger = logging.getLogger(__name__)

def register(request):
    logger.info(f"Register view accessed with method: {request.method}")
    if request.user.is_authenticated:
        logger.info("User is already authenticated, redirecting to dashboard.")
        return redirect('products:dashboard')
    if request.method == 'POST':
        logger.info("Processing POST request for registration.")
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            logger.info("Registration form is valid. Saving user.")
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            logger.info("User registered and logged in. Redirecting to dashboard.")
            return redirect('products:dashboard')
        else:
            logger.warning("Registration form is invalid. Errors: %s", form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        logger.info("Processing GET request for registration.")
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('products:dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('products:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('users:login')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form}) 