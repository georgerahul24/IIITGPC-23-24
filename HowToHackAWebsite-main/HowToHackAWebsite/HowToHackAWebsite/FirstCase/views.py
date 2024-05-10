from django.shortcuts import render
from django.views import View
from .forms import *
from AppDataModels.models import UsernameAndPassword


class FirstCase(View):
    def get(self, request):
        return render(request, 'logInFirstCase.html')

    def post(self, request):
        loginForm = FirstCaseForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']

            try:
                # Just check if the username and the password is matching
                UsernameAndPassword.objects.get(username=username, password=password)
                return render(request, 'success.html')
            except UsernameAndPassword.DoesNotExist:
                return render(request, 'failed.html')

        return render(request, 'failed.html')
