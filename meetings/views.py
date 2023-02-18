from django.contrib import messages
from django.contrib.auth import logout as django_logout, authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from core.models import User


class DashboardView(TemplateView):
    login_url = "/"
    template_name = "dashboard.html"
    __doc__ = "This view is used to redirect for dashboard page"


class LoginView(TemplateView):
    login_url = "/"
    template_name = "login.html"
    __doc__ = "This view is used to redirect for login page"

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard')
        else:
            messages.add_message(
                request, messages.INFO, "Username or Password is incorrect."
            )
            return redirect("/dashboard")


def logout(request):
    django_logout(request)
    return redirect("/dashboard")


class MyMeetingView(TemplateView):
    login_url = "/"
    template_name = "my_meeting.html"
    __doc__ = "This view is used to get the details of owner meeting"