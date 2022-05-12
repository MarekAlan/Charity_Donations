from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from charity_app.forms import CreateUserForm, LoginForm, UpdateUserForm
from charity_app.models import Institution, Donation, Category


class LandingPageView(View):

    def get(self, request):
        nb_bags = 0
        donations = Donation.objects.all()
        for donation in donations:
            nb_bags += donation.quantity
        nb_organizations = Institution.objects.all().count()
        foundations_list = Institution.objects.all().filter(type="Fundacja").order_by('id')
        paginator = Paginator(foundations_list, 5)
        page = request.GET.get('page')
        foundations = paginator.get_page(page)
        ctx = {
            "foundations": foundations,
            "ngos": Institution.objects.all().filter(type="Organizacja Pozarządowa"),
            "local": Institution.objects.all().filter(type="Zbiórka Lokalna"),
            "nb_bags": nb_bags,
            "nb_organizations": nb_organizations,
        }
        return render(request, 'index.html', ctx)


class AddDonationView(LoginRequiredMixin, View):

    login_url = 'login'

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {
            'categories': categories,
            'institutions': institutions
        }
        return render(request, 'form.html', ctx)

    def post(self, request):
        return redirect('index')


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,
                                password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        return redirect('register')


class RegisterView(View):

    def get(self, request):
        form = CreateUserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(
                form.cleaned_data['pass1'])
            user.username = form.cleaned_data['email']
            user.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})


class LogOutView(View):

    def get(self, request):
        logout(request)
        return redirect('index')


class UserView(View):

    def get(self, request):
        user_id = request.user.id
        donations = Donation.objects.all().filter(user_id=user_id)
        for donation in donations:
            categories = donation.categories.all()
        ctx = {
            "user_id": user_id,
            "donations": donations,
            "categories": categories,
        }
        return render(request, 'user.html', ctx)


class UpdateUserView(View):

    def get(self, request):
        form_user = UpdateUserForm(instance=request.user)
        form = PasswordChangeForm(request.user)
        return render(request, 'update_user.html', {'form_user': form_user, 'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Twoje hasło zostało zmienione')
            return redirect('change_password')
        else:
            messages.error(request, 'Spróbuj jeszcze raz.')

        form_user = UpdateUserForm(request.POST, instance=request.user)
        if form_user.is_valid():
            user = form_user.save(commit=False)
            user.username = form_user.cleaned_data['email']
            user.save()
            return redirect('login')
        return render(request, 'update_user.html', {'form_user': form_user, 'form': form})


# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             messages.success(request, 'Twoje hasło zostało zmienione')
#             return redirect('change_password')
#         else:
#             messages.error(request, 'Spróbuj jeszcze raz.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'update_user.html', {
#         'form': form
#     })