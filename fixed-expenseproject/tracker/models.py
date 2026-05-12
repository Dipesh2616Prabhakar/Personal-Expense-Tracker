from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):
    TYPE_CHOICES = [('expense', 'Expense'), ('income', 'Income')]

    CATEGORY_CHOICES = [
        ('Food', 'Food'), ('Transport', 'Transport'), ('Shopping', 'Shopping'),
        ('Health', 'Health'), ('Entertainment', 'Entertainment'), ('Bills', 'Bills'),
        ('Education', 'Education'), ('Salary', 'Salary'), ('Freelance', 'Freelance'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Other')
    date = models.DateField()                          # Fixed: no auto_now_add — user sets date
    txn_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='expense')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.txn_type}) — ₹{self.amount}"
