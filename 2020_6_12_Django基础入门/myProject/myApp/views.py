# myApp/views.py
from django.shortcuts import render
from django.http import HttpResponse
from myApp.models import Book

# myApp/views.py
from django.http import HttpResponseRedirect
from django.urls import reverse

def addBook(request):
    if request.method == 'POST':
        temp_name = request.POST['name']
        temp_author = request.POST['author']
        temp_pub_house = request.POST['pub_house']

    from django.utils import timezone
    temp_book = Book(name=temp_name, author=temp_author, pub_house=temp_pub_house, pub_date=timezone.now())
    temp_book.save()

    # 重定向
    return HttpResponseRedirect(reverse('detail'))
def detail(request):
    book_list = Book.objects.order_by('-pub_date')[:5]
    context = {'book_list': book_list}
    return render(request, 'myApp/detail.html', context)
# myApp/views.py
def deleteBook(request, book_id):
    bookID = book_id
    Book.objects.filter(id=bookID).delete()

    # 重定向
    return HttpResponseRedirect(reverse('detail'))