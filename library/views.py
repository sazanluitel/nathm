from django.shortcuts import render, redirect
from django.views import View
from .forms import BookForm, LibraryForm

class BookView(View):
    def post(self, request, *args, **kwargs):
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('library_admin_urls:books')
        else:
            return render(request, 'dashboard/library/book.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = BookForm()
        return render(request, 'dashboard/library/book.html', {'form': form})

        


class LibraryView(View):
    def get(self, request, *args, **kwargs):
        form = LibraryForm
        return render(request, 'dashboard/library/library.html', {'form': form})