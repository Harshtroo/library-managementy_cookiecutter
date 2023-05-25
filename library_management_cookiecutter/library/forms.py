from typing import Any, Dict

from base.constance import Role
from django import forms
from django.contrib.auth.models import User

from .models import AssignedBook, Book, User


class UserForm(forms.ModelForm):
    """user forms"""

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        """userform meta class"""

        model = User
        fields = ["first_name", "last_name", "email", "username", "role"]

    def save(self, commit=False):
        instance = super().save(commit=True)
        instance.set_password(instance.username + "@1234")
        if commit:
            instance.save()
        return instance


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["book_image", "book_name", "author_name", "price", "quantity"]


class AsignBookForm(forms.ModelForm):
    class Meta:
        model = AssignedBook
        fields = ["user", "book"]
