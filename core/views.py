from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.http import HttpResponse
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import FormView



class HomeView(View):
    def get(self, request):
        return render(request, 'core/home.html')


class RegisterView(View):
    template_name = 'core/register.html'
    form_class = UserCreationForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')  # Use 'password1' field for password
            user = authenticate(request, username=username, password=raw_password)
            if user:
                login(request, user)
                messages.success(request, "Registration Successful")
                return redirect('login')
        messages.error(request, "Registration Failed, Please Try Again")
        return render(request, self.template_name, {'form': form})



class UserLoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'core/login.html'
    success_url = reverse_lazy('home')  # Use reverse_lazy to defer URL resolution

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome Back {username}")
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid Username and Password")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid Username and Password")
        return super().form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home') 



