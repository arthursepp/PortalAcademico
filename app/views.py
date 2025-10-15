from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *

def index(request):
    # * Se o usuário já estiver autenticado, redireciona para a página principal
    if request.user.is_authenticated:
        return redirect('portal')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # * Autentica o usuário
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('portal')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'index.html')

@login_required
def portal(request):
    # * Página principal após login
    context = {
        'user': request.user
    }
    return render(request, 'portal.html')  # * Você precisará criar este template

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('index')