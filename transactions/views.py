from django.shortcuts import render , redirect
from datetime import datetime
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login , authenticate , logout
from django.contrib import messages
from django.views.decorators.cache import never_cache


@login_required
def dashboard(request):

    month = request.GET.get("month")

    # If no month selected → use current month

    if not month:
        now = datetime.now()
        month = f"{now.year}-{str(now.month).zfill(2)}"

    year, month_number = month.split("-")

    # Filter by selected month
    transactions = Transaction.objects.filter(
        user= request.user,
        transaction_date__year=int(year),
        transaction_date__month=int(month_number)
    )

    # POST Method

    if request.method == "POST":

        form_type = request.POST.get("form_type")

        # Category Form
        if form_type == "category":

            category_name = request.POST.get("category_name")
            category_type = request.POST.get("category_type")

            if category_name and category_type:

                Category.objects.create(
                    user=request.user,
                    name=category_name,
                    type=category_type
                )

            return redirect("dashboard")

        # Transaction Form
        elif form_type == "transaction":

            category = request.POST.get("category")
            amount = request.POST.get("amount")
            t_type = request.POST.get("type")
            transaction_date = request.POST.get("date")

            if category and amount and t_type and transaction_date:

                Transaction.objects.create(
                    user=request.user,
                    category=category,
                    amount=amount,
                    type=t_type,
                    transaction_date=transaction_date
                )

        elif form_type == "budget":
            print("BUDGET SAVED")
            category_id = request.POST.get("budget_category")
            amount = request.POST.get("budget_amount")
            month = request.POST.get("budget_month")
            year = request.POST.get("budget_year")

            category = Category.objects.get(id=category_id)

            Budget.objects.create(
                user=request.user,
                category=category,
                amount=amount,
                month=month,
                year=year
            )

            return redirect("dashboard")
            
    # transactions = Transactions.objects.all()

    income_total = 0
    expense_total = 0
    income_categories = {}
    expense_categories = {}

    for t in transactions:
        if t.type == "income":
            income_total +=t.amount
            if t.category in income_categories:
                income_categories[t.category] += t.amount
            else:
                income_categories[t.category] = t.amount

        else:
            expense_total += t.amount
            if t.category in expense_categories:
                expense_categories[t.category] += t.amount
            else:
                expense_categories[t.category] = t.amount

    balance = income_total - expense_total


    income_categories_list = Category.objects.filter(
    user=request.user,
    type="income")

    expense_categories_list = Category.objects.filter(
        user=request.user,
        type="expense"
    )
    budgets = Budget.objects.filter(
    user=request.user,
    month=int(month_number),
    year=int(year)
    )

    budget_data = []

    for budget in budgets:

        spent = Transaction.objects.filter(
            user=request.user,
            category=budget.category.name,
            type="expense",
            transaction_date__month=int(month_number),
            transaction_date__year=int(year)
        )

        total_spent = sum(t.amount for t in spent)

        percentage = 0

        if budget.amount > 0:
            percentage = min(
                (total_spent / budget.amount) * 100,
                100
            )

        budget_data.append({
            "category": budget.category.name,
            "budget": budget.amount,
            "spent": total_spent,
            "percentage": percentage
        })
    
    return render(request, "transactions/dashboard.html", {
    "income_total": income_total,
    "expense_total": expense_total,
    "balance": balance,
    "income_categories": income_categories,
    "expense_categories": expense_categories,
    "selected_month": month,

    "income_categories_list": income_categories_list,
    "expense_categories_list": expense_categories_list,
    "selected_month": month,

    "budget_data": budget_data,
})


@login_required
@never_cache
def transaction(request):

    month = request.GET.get("month")

    # ✅ STEP 1: If no month → use current month
    if not month:
        now = datetime.now()
        month = f"{now.year}-{str(now.month).zfill(2)}"

    # ✅ STEP 2: Now safe to split
    year, month_number = month.split("-")

    # ✅ STEP 3: Filter only logged-in user + selected month
    transactions = Transaction.objects.filter(
        user=request.user,
        transaction_date__year=int(year),
        transaction_date__month=int(month_number)
    ).order_by("-transaction_date")

    # ✅ STEP 4: Handle edit
    if request.method == "POST":
        transaction_id = request.POST.get("transaction_id")

        if transaction_id:
            transaction = Transaction.objects.get(
                id=transaction_id,
                user=request.user   # security
            )

            transaction.category = request.POST.get("category")
            transaction.amount = request.POST.get("amount")
            transaction.transaction_date  = request.POST.get("date")
            transaction.save()

            return redirect(f"/transaction/?month={month}")

    return render(request, "transactions/transaction.html", {
        "transactions": transactions,
        "selected_month": month
    })

def delete_transaction(request , id):
    transaction = Transaction.objects.get(id=id)
    transaction.delete()
    return redirect("/transaction/")
    
@never_cache
def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")
        
        if User.objects.filter(username=username).exists():
            
            username = request.POST.get("username")
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            if password1 != password2:
                messages.error(request, "Passwords do not match")
                return redirect("register")
            
        user=User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Account created successfully!")
        return redirect("login")


    return render(request , "transactions/register.html")

@never_cache
def user_login(request):

    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "transactions/login.html")


@login_required
def manage(request):

    income_categories = Category.objects.filter(
        user=request.user,
        type="income"
    )

    expense_categories = Category.objects.filter(
        user=request.user,
        type="expense"
    )

    return render(request, "transactions/manage.html", {
        "income_categories": income_categories,
        "expense_categories": expense_categories,
    })


@login_required
def delete_category(request, id):

    category = Category.objects.get(
        id=id,
        user=request.user
    )

    transaction_exists = Transaction.objects.filter(
        user=request.user,
        category=category.name
    ).exists()

    if transaction_exists:
        messages.error(
            request,
            f"Cannot delete '{category.name}' because transactions are using it."
        )
        return redirect("manage")

    category.delete()

    messages.success(
        request,
        f"Category '{category.name}' deleted successfully."
    )

    return redirect("manage")

@never_cache
def user_logout(request):
    logout(request)
    return redirect("login")