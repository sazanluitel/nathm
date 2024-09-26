from django.shortcuts import render
from django.views import View
from .forms import BookForm, LibraryForm

class BookView(View):
    def get(self, request):
        form = BookForm
        return render(request, 'dashboard/library/book.html', {'form': form})


class LibraryView(View):
    def get(self, request, *args, **kwargs):
        form = LibraryForm
        return render(request, 'dashboard/library/library.html', {'form': form})