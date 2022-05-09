from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from charity_app.forms import CreateUserForm, LoginForm
from charity_app.models import Institution, Donation


class LandingPageView(View):

    def get(self, request):
        nb_bags = 0
        donations = Donation.objects.all()
        for donation in donations:
            nb_bags += donation.quantity
        nb_organizations = Institution.objects.all().count()
        institution_list = Institution.objects.all().order_by('id')
        paginator = Paginator(institution_list, 5)
        page = request.GET.get('page')
        institutions = paginator.get_page(page)
        ctx = {
            'institutions': institutions,
            "foundations": Institution.objects.all().filter(type="Fundacja"),
            "ngos": Institution.objects.all().filter(type="Organizacja Pozarządowa"),
            "local": Institution.objects.all().filter(type="Zbiórka Lokalna"),
            "nb_bags": nb_bags,
            "nb_organizations": nb_organizations,
        }
        return render(request, 'index.html', ctx)


class AddDonationView(View):

    def get(self, request):
        return render(request, 'form.html')


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



