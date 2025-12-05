from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import os

User = get_user_model()


def create_admin_view(request):
    """
    Public view to create the first admin user.
    Only works if no superusers exist yet.
    """
    # Check if any superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        return render(request, 'home/admin_exists.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validation
        if not all([username, email, password, password_confirm]):
            messages.error(request, 'All fields are required.')
            return render(request, 'home/create_admin.html')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'home/create_admin.html')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'home/create_admin.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'home/create_admin.html')
        
        # Create superuser
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, f'Admin user "{username}" created successfully! You can now login.')
            return redirect('/admin/')
        except Exception as e:
            messages.error(request, f'Error creating admin user: {str(e)}')
            return render(request, 'home/create_admin.html')
    
    return render(request, 'home/create_admin.html')
