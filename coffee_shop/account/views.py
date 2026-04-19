from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms
from django.contrib.auth.models import User
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')   # change to your URL name
        else:
            return render(request, 'account/login.html', {
                'error': 'Invalid username or password'
            })


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")


class CoffeeCornerRegisterView(View):
    template_name = 'coffee_corner/register.html'

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Welcome to Coffee Corner ☕')
            login(request, user)
            return redirect('home')  # Change to your home page
        return render(request, self.template_name, {'form': form})