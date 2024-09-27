from django.urls import path
from .views import LibraryView, BookView, BookAjaxView,LibraryAjaxView

app_name = 'library_admin_urls'

urlpatterns = [
    path('library/', LibraryView.as_view(), name='library'),
    path('library/edit/<id>/', LibraryView.as_view(), name='libraryedit'),
    path('library/ajax/', LibraryAjaxView.as_view(), name='libraryajax'), 

    path('books/', BookView.as_view(), name='books'), 
    path('books/edit/<id>/', BookView.as_view(), name='edit'), 
    path('books/ajax/', BookAjaxView.as_view(), name='ajax'), 
]
