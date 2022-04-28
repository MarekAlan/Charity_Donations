from django.shortcuts import render

# Create your views here.
from django.views import View

from charity_app.models import Institution, Donation


class LandingPageView(View):

    def get(self, request):
        nb_bags = 0
        donations = Donation.objects.all()
        for donation in donations:
            donation.quantity += nb_bags
        nb_organizations = Institution.objects.all().count()
        ctx = {
            "nb_bags": nb_bags,
            "nb_organizations": nb_organizations,
        }
        return render(request, 'index.html', ctx)


class AddDonationView(View):

    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')



