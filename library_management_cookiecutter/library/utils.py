from django.db.models import Count

from .models import AssignedBook, Book, User


def bookHistory():
    assigned_books = AssignedBook.objects.values("book").annotate(count=Count("book"))
    book_list = []
    for assigned_book in assigned_books:
        book = Book.objects.get(id=assigned_book["book"])
        assign_username = AssignedBook.objects.filter(
            book=book, is_deleted=False
        ).values_list("user__username", flat=True)
        assignments_count = assign_username.count()
        return_name = AssignedBook.objects.filter(
            book=book, is_deleted=True
        ).values_list("user__username", flat=True)
        returns_count = return_name.count()

        book_list.append(
            {
                "name": book.book_name,
                "assign_count": assignments_count,
                "return_count": returns_count,
                "assign_user": list(assign_username),
                "return_name": list(return_name),
            }
        )
    return book_list
