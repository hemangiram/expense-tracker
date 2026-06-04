from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
import csv
from django.http import HttpResponse
from .models import Expense
from .forms import ExpenseForm




# ---------------- AUTH ----------------
def signup(request):
    if request.method == "POST":
        print("@@@@@@@@@@@@")
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password,"$$$$$$$$$$$$")

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            print(User.objects.create_user, "!!!!!!!!!!!!!!!!!!!!")
        return redirect("login_viewer")

    return render(request, "expense/signup.html")




def login_view(request):
    if request.method == "POST":
        print("[{...................}]")
        username = request.POST["username"]
        password = request.POST["password"]
        print("###############")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("expense_list")

    return render(request, "expense/login.html")





@login_required
def logout_view(request):
    logout(request)
    print(logout)
    return redirect("login_viewer")



# ---------------- DASHBOARD ----------------


@login_required
def dashboard(request):
    category_query = request.GET.get("category")
    payment_query = request.GET.get("payment_method")

    # ONLY logged-in user's expenses
    expenses = Expense.objects.filter(user=request.user).order_by("-date")

    if category_query:
        expenses = expenses.filter(category=category_query)

    if payment_query:
        expenses = expenses.filter(payment_method=payment_query)

    total_amount = expenses.aggregate(Sum("amount"))["amount__sum"] or 0

    # ADD EXPENSE

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # IMPORTANT FIX
            expense.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm()

    context = {
        "expenses": expenses,
        "total_amount": total_amount,
        "form": form,
        "categories": [c[0] for c in Expense.CATEGORY_CHOICES],
        "selected_category": category_query,
        "payment_query": payment_query,
    }

    return render(request, "expense/index.html", context)


# ---------------- DELETE ----------------





@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    expense.delete()
    return redirect("expense_list")


# ---------------- EDIT ----------------





@login_required
def edit_transaction(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm(instance=expense)

    return render(
        request, "expense/edit_expense.html", {"form": form, "expense": expense}
    )





@login_required
def export_csv(request):
    # Only logged-in user's expenses
    expenses = Expense.objects.filter(user=request.user).order_by("-date")

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="expenses.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["Title", "Amount", "Category", "Date", "Payment Method"])

    for e in expenses:
        writer.writerow([e.title, e.amount, e.category, e.date, e.payment_method])

    return response
