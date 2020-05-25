from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate
from .forms import UserCreationForm, AccountForm

# Create your views here.
def signup(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        form = AccountForm(request.POST)
        if user_form.is_valid() and form.is_valid():
            user = user_form.save()

            account = form.save(commit=False)
            account.user = user

            account.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect('home')

    else:
        user_form = UserCreationForm()
        form = AccountForm()
    return render(request, 'accounts/signup.html', {'user_form': user_form, 'form': form})



def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'id 혹은 비밀번호가 틀렸습니다.'})
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')
