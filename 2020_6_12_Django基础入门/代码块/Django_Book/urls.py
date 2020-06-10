from django.contrib import admin
from django.urls import path
from myApp import views

app_name = 'myApp'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.detail, name='detail'),
    path('addBook/', views.addBook, name='addBook'),
    path('delBook/<int:book_id>', views.deleteBook, name='delBook'),
]