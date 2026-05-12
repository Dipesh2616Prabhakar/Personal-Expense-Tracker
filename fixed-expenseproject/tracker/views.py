from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Expense
from django.db.models import Sum
import json


@login_required
def dashboard(request):
    if request.method == "POST":
        title = request.POST.get('title', '').strip()
        amount = request.POST.get('amount', 0)
        category = request.POST.get('category', 'Other')
        date = request.POST.get('date')
        txn_type = request.POST.get('type', 'expense')

        if title and amount and date:
            Expense.objects.create(
                user=request.user,
                title=title,
                amount=float(amount),
                category=category,
                date=date,
                txn_type=txn_type
            )
        return redirect('dashboard')   # PRG pattern — prevents duplicate on refresh

    expenses = Expense.objects.filter(user=request.user).order_by('-date', '-id')

    total_income = expenses.filter(txn_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expenses.filter(txn_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    context = {
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('dashboard')
    return redirect('dashboard')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)          # auto-login after signup
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    error = None
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid username or password."
    return render(request, 'tracker/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'tracker/landing.html')
