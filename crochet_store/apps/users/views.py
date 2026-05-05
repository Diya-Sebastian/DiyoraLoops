from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.role == 'seller':
                user.is_active = False
                user.save()
                messages.info(request, "Your seller account has been created and is pending admin approval.")
                return redirect('users:login')
            
            user.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('products:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active:
                    messages.error(request, "Your account is deactivated. Please contact the administrator.")
                    return redirect('users:login')
                
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                if user.role == 'admin':
                    return redirect('admin_custom:dashboard')
                elif user.role == 'seller':
                    return redirect('seller_custom:dashboard')
                else:
                    return redirect('products:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    is_admin = request.user.is_authenticated and request.user.role == 'admin'
    logout(request)
    messages.success(request, "You have been logged out.")
    if is_admin:
        return redirect('users:login')
    return redirect('products:home')
