from django.shortcuts import render, redirect
from django.views import View
from .forms import BookForm, LibraryForm
from django.contrib import messages
from .models import Book, Library
from students.models import Student
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse


class BookView(View):
    def post(self, request, *args, **kwargs):
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully')
            return redirect('library_admin_urls:books')
        else:
            messages.error(request, 'Error in the forms')
            return render(request, 'dashboard/library/book.html', {'form': form})
    def get(self, request, *args, **kwargs):
        form = BookForm()
        return render(request, 'dashboard/library/book.html', {'form': form})


class BookAjaxView(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        program_id = request.GET.get("program", None)
        page_number = (start // length) + 1

        # Select the books, and order them by the most recent
        books = Book.objects.select_related('program').order_by("-id")

        # Filter based on program ID
        if program_id:
            books = books.filter(program_id=program_id)

        # Filter based on search value across multiple fields
        if search_value:
            books = books.filter(
                Q(name__icontains=search_value) |
                Q(author__icontains=search_value) |
                Q(publication_house__icontains=search_value) |
                Q(program__name__icontains=search_value)
            )

        # Paginate the results
        paginator = Paginator(books, length)
        page_books = paginator.page(page_number)

        # Build the data to send to DataTables
        data = []
        for book in page_books:
            data.append([
                book.name,
                self.get_action(book)
            ])

        # Return JSON response
        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, book):
        book_id = book.id
        edit_url = reverse('library_admin_urls:edit')
        delete_url = reverse('dashboard:delete')

        return f'''
            <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
            <a href="{delete_url}" class="btn btn-danger btn-sm">Delete</a>
        '''
class EditBookView(View):
    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('_selected_id')
        book = Book.objects.get(id=book_id)
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully')
            return redirect('library_admin_urls:books')
        else:
            messages.error(request, 'Error in the forms')
            return render(request, 'dashboard/library/book.html', {'form': form})
        
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = Book.objects.get(id=book_id)
        form = BookForm(instance=book)
        return render(request, 'dashboard/library/book.html', {'form': form})

class LibraryView(View):
    def post(self, request, *args, **kwargs):
        form = LibraryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Library added successfully')
            return redirect('library_admin_urls:library')
        else:
            messages.error(request, 'Error in the forms')
            return render(request, 'dashboard/library/library.html', {'form': form})
    def get(self, request, *args, **kwargs):
        form = LibraryForm()
        return render(request, 'dashboard/library/library.html', {'form': form})