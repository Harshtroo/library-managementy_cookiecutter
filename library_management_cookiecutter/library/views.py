import csv
import os
import zipfile
from io import StringIO

import pyminizip
from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import EmailMessage
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, FormView, ListView, TemplateView
from .forms import AddBookForm, AsignBookForm, UserForm
from .mixin import MyCustomPermissions
from .models import AssignedBook, Book, User
from .utils import bookHistory


class Home(TemplateView):
    template_name = "home.html"


class Login(LoginView):
    """login class"""

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "success"})
        return JsonResponse({"message": "username and password not match."}, status=400)


class Logout(LogoutView):
    """logout class"""
    pass


class CreateUser(CreateView):
    template_name = "create_user.html"
    form_class = UserForm

    def post(self, request, *args, **kwargs):
        """create user post request"""
        user_form = self.form_class(request.POST or None)

        if user_form.is_valid():
            user = user_form.save()
            user.save()
            user_role = user.role
            group = Group.objects.get(name=user_role)
            user.groups.add(group.id)
            messages.success(self.request, "successfully register.")
            return JsonResponse({"message": "success"})
        return JsonResponse({"message": user_form.errors}, status=400)


class AddBooks(LoginRequiredMixin, MyCustomPermissions, CreateView):
    """add book"""

    login_url = "login"
    template_name = "add_book.html"
    form_class = AddBookForm
    permission_required = {"GET": ["library.add_book"]}

    def post(self, request, *args, **kwargs):
        book_form = self.form_class(request.POST, request.FILES)
        if book_form.is_valid():
            book = book_form.save(commit=False)
            book.available_quantity = book_form.cleaned_data.get("quantity")
            book.save()
            messages.success(request, "successfully add book.")
            return JsonResponse({"message": "success"})
        return JsonResponse({"message": book_form.errors}, status=400)


class SuccessMessage(TemplateView):
    """success class"""

    template_name = "successpage.html"


class BookList(FormView):
    """book list show"""

    login_url = "login"
    model = Book
    template_name = "book_list.html"
    form_class = AsignBookForm

    def get(self, request, *args, **kwargs):
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            result = dict()
            data_list = []
            result["status"] = "success"
            for books in Book.objects.all():
                total_books_assign = AssignedBook.objects.filter(
                    book=books, is_deleted=False
                ).count()
                rem = books.quantity - total_books_assign
                book_list = {
                    "id": books.id,
                    "book_image": books.book_image.url,
                    "book_name": books.book_name,
                    "author_name": books.author_name,
                    "quantity": books.quantity,
                    "available": rem,
                }
                data_list.append(book_list)
            return JsonResponse(data_list, safe=False)
        return render(request, "book_list.html", context={"users": User.objects.all()})

    def post(self, request, *args, **kwargs):
        form = AsignBookForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.POST.get("user"))
            book = Book.objects.get(id=request.POST.get("book"))
            btn_action = request.POST.get("btn_action")

            if btn_action == "assign_book":
                if AssignedBook.objects.filter(book=book, user=user, is_deleted=False):
                    return JsonResponse(
                        status=400, data={"message": "already book assign."}
                    )

                assignment = form.save(commit=False)
                assignment.user = user
                assignment.save()

                total_books_assign = AssignedBook.objects.filter(
                    book=book, is_deleted=False
                ).count()
                rem = book.quantity - total_books_assign
                return JsonResponse(
                    {
                        "message": "successfully book assign.",
                        "rem": rem,
                        "book_id": book.id,
                    }
                )


class AssignBookUser(View):
    template_name = "user_assign_book_list.html"
    model = AssignedBook
    queryset = AssignedBook.objects.filter(is_deleted=False)

    def get(self, request, *args, **kwargs):
        assign_book_list = list(
            AssignedBook.objects.filter(user=request.user, is_deleted=False)
        )
        assign_book_data = [
            {"id": assign_book.book.id, "book": assign_book.book.book_name}
            for assign_book in assign_book_list
        ]
        return render(
            self.request,
            self.template_name,
            context={"assign_book_data": assign_book_data},
        )

    def post(self, request, *args, **kwargs):
        user = request.user
        book = Book.objects.get(id=request.POST.get("book"))

        if AssignedBook.objects.filter(book=book, user=user, is_deleted=False).exists():
            if request.POST.get("button_action") == "return_book":

                assigned_book = AssignedBook.objects.get(
                    book=book, user=user, is_deleted=False
                )
                assigned_book.is_deleted = True
                assigned_book.date_returned = timezone.now()
                assigned_book.save()

                response = {
                    "status": True,
                    "message": "Book Returened successfully",
                }
                return JsonResponse(response, safe=False)
            else:
                data_list = []
                for books in AssignedBook.objects.filter(book=book, user=user):
                    book_list = {
                        "date_borrowed": books.date_borrowed,
                        "date_return": books.date_returned,
                    }
                    data_list.append(book_list)
                return JsonResponse(data_list, safe=False)
        else:
            return JsonResponse({"message": "done"})


class BookHistory(TemplateView):
    template_name = "book_history.html"
    model = AssignedBook

    def post(self, request, *args, **kwargs):
        book_list = bookHistory()
        return JsonResponse({"book_list": book_list})


def exportcsv(request):
    user = AssignedBook.objects.all()
    response = HttpResponse("text/csv")
    response["Content-Disposition"] = "attachment; filename=user.csv"
    writer = csv.writer(response)
    writer.writerow(["User Name", "book name", "assign date", "return date"])
    user_details = user.values_list(
        "user__first_name",
        "user__last_name",
        "book__book_name",
        "date_borrowed__date",
        "date_returned__date",
    )

    csv_data = StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(["User Name", "book name", "assign date", "return date"])

    for details in user_details:
        full_name = f"{details[0]} {details[1]}"
        writer.writerow([full_name, details[2], details[3], details[4]])

    zip_filename = "harsh.zip"
    zip_password = request.user.email

    with open("harsh.csv", "w") as f:
        f.write(csv_data.getvalue())
    pyminizip.compress("harsh.csv", "zip", zip_filename, zip_password, 0)

    email = EmailMessage(
        subject="CSV Export",
        body="Please find the attached zip file.",
        from_email="harsh.vekariya@trootech.com",
        to=[request.user.email],
    )

    with open(zip_filename, "rb") as file:
        email.attach(zip_filename, file.read(), "application/zip")

    email.send()
    os.remove(zip_filename)
    messages.success(request, "successfully send email.")
    return redirect("/")
