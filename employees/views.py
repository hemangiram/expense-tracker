from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from .forms import EmployeeForm
from .models import Employee
from django.core.paginator import Paginator  # type: ignore
from django.db.models import Q  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.contrib.auth.models import Group, User
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import user_passes_test  # type: ignore


def is_admin(user):
    return user.is_superuser or user.groups.filter(name="Admin").exists()


def signup(request):
    if request.method == "POST":
        print("@@@@@@@@@@@@")
        form = SignUpForm(request.POST)
        print("form")
        if form.is_valid():
            print("form valid")
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            group, created = Group.objects.get_or_create(name="User")
            print(group,created,"$$$$$$$$$$$$$$$")
            user.groups.add(group)
            print("##############")

            login(request, user)
            print(login, "***************")
            return redirect("login_user")
    else:
        form = SignUpForm()

    return render(request, "employee/signup.html", {"form": form})


@login_required
def emp_list(request):
    query = request.GET.get("q", "").strip()  # search term
    if query:
        employees_list = Employee.objects.filter(
            Q(name__icontains=query) | Q(email__icontains=query)
        )
    else:
        employees_list = Employee.objects.all()

    paginator = Paginator(employees_list, 3)
    page_number = request.GET.get("page")
    employees = paginator.get_page(page_number)

    return render(
        request, "employee/emp_list.html", {"employees": employees, "query": query}
    )


@login_required
@user_passes_test(is_admin)
def emp_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("emp_list")
    else:
        form = EmployeeForm()
        return render(request, "employee/emp_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def emp_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect("emp_list")
    else:
        form = EmployeeForm(instance=employee)
        return render(request, "employee/emp_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def emp_del(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        employee.delete()
        return redirect("emp_list")
    return render(request, "employee/emp_del.html", {"employee": employee})
