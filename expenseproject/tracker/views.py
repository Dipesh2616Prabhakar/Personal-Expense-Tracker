# Create yours views here
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm
from .models import Expense

@login_required
def dashboard(request):

    if request.method == "POST":
        Expense.objects.create(
            user=request.user,
            title=request.POST['title'],
            amount=request.POST['amount'],
            category=request.POST['category'],
            date=request.POST['date']
        )

    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    return render(request,'dashboard.html',{'expenses':expenses})


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect("login")