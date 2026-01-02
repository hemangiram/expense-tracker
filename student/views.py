from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm


def stud_list(request):
    students = Student.objects.all()
    return render(request, "students/stud_list.html", {"students": students})


def stud_add(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("stud_list")
    else:
        form = StudentForm()
        return render(request, "students/stud_form.html", {"form": form})


def stud_edit(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("stud_list")
    else:
        form = StudentForm(instance=student)
        return render(request, "students/stud_form.html", {"form": form})


def stud_del(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        student.delete()
        return redirect("stud_del")
    return render(request, "students/stud_del.html", {"student": student})
