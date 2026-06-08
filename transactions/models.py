from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Transaction(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    transaction_types = (
        ('income' , 'Income'),
        ('expense' , 'Expense')
    )
    category = models.CharField(max_length=50)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    type = models.CharField(max_length=10 , choices=transaction_types)

    note = models.TextField(blank=True  , null = True)

    transaction_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add = True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.amount}"
    



# ================
# Category-Model 
# ===============
class Category(models.Model):

    CATEGORY_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=50)

    type = models.CharField(
        max_length=10,
        choices=CATEGORY_TYPES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
    

# ==========================
# Budget model
# ==========================


class Budget(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE , 
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    month = models.IntegerField()

    year = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.category.name} - {self.amount}"