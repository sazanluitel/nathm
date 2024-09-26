from django.urls import path
from .views import LibraryView, BookView, BookAjaxView,EditBookView

app_name = 'library_admin_urls'

urlpatterns = [
    path('library/', LibraryView.as_view(), name='library'),
    path('books/', BookView.as_view(), name='books'), 
    path('bookedit/', EditBookView.as_view(), name='edit'), 
    path('booksajax/', BookAjaxView.as_view(), name='ajax'), 
]
