from django.shortcuts import get_object_or_404, render, redirect
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
        id = kwargs.get("id", None)
        if id:
            book = Book.objects.get(id=id)
            form = BookForm(request.POST, instance=book)
        else:
            form = BookForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully')
            return redirect('library_admin_urls:books')
        else:
            messages.error(request, 'Error in the forms')
            return render(request, 'dashboard/library/book.html', {'form': form})
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if id:
            book = Book.objects.get(id=id)
            form = BookForm(instance=book)
        else:
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
                self.get_action(book.id)
            ])

        # Return JSON response
        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)
    def get_action(self, book_id):
        edit_url = reverse('library_admin_urls:edit', kwargs={'id': book_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('library_admin_urls:books')
        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>

                <input type="hidden" name="_selected_id" value="{book_id}" />
                <input type="hidden" name="_selected_type" value="book" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''
class LibraryView(View):
    def post(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if id:
            library = Library.objects.get(id=id)
            form = LibraryForm(request.POST, instance=library)
        else:
            form = LibraryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Library added successfully')
            return redirect('library_admin_urls:library')
        else:
            messages.error(request, 'Error in the forms')
            return render(request, 'dashboard/library/library.html', {'form': form})
        
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if id:
            library = Library.objects.get(id=id)
            form = LibraryForm(instance=library)
        else:
            form = LibraryForm()
        return render(request, 'dashboard/library/library.html', {'form': form})
    
class LibraryAjaxView(View):
    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        libraries = Library.objects.all()

        paginator = Paginator(libraries, length)
        page_books = paginator.page(page_number)

        data = []
        for library in page_books:
            data.append([
                library.borrowed_by.email, 
                library.book.name,          
                library.get_status_display(), 
                self.get_action(library) 
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,  
            "data": data,
        }, status=200)

    def get_action(self, library):
        edit_url = reverse('library_admin_urls:libraryedit', kwargs={'id': library.id})
        delete_url = reverse('generic:delete')
        approve_url = reverse('library_admin_urls:approve', kwargs={'id': library.id})
        backurl = reverse('library_admin_urls:library')

        # If the status is approved, disable the approve button
        approve_button = f'''
            <a href="{approve_url}" class="btn btn-primary btn-sm">Approve</a>
        ''' if library.status == 'pending' else '''
            <button class="btn btn-secondary btn-sm" disabled>Approved</button>
        '''

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <input type="hidden" name="_selected_id" value="{library.id}" />
                <input type="hidden" name="_selected_type" value="library" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                {approve_button}
            </form>
        '''


class ApproveLibraryView(View):
    def post(self, request, id):
        library = get_object_or_404(Library, id=id)
        library.status = 'approved'
        library.save()
        messages.success(request, 'Library approved successfully')
