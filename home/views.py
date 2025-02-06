import requests
from .models import *
from .forms import RegisterForm, LoginForm


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Sum


# Asosiy sahifa (faqat login qilingan foydalanuvchilarga)
@login_required(login_url='login')  # Login shart
def index_page(request):
    context = {
        'books_list': Book.objects.filter(is_popular=False),
        'pop_books_list': Book.objects.filter(is_popular=True),
    }
    return render(request, 'index.html', context=context)


def index2_page(request):
    context = {
        'books_list': Book.objects.filter(is_popular=False),
        'pop_books_list': Book.objects.filter(is_popular=True),
    }
    return render(request, 'index-2.html', context=context)


# Tizimga kirish
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Xush kelibsiz, {user.username}!')
                return redirect('index')  # Tizimga kirgach asosiy sahifaga o'tadi
            else:
                messages.error(request, 'Login yoki parol noto‘g‘ri!')
        else:
            messages.error(request, 'Formani to‘g‘ri to‘ldiring!')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# Ro‘yxatdan o‘tish
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Ro‘yxatdan muvaffaqiyatli o‘tdingiz!')
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


# Tizimdan chiqish
def logout_view(request):
    logout(request)
    messages.success(request, 'Tizimdan muvaffaqiyatli chiqdingiz!')
    return redirect('login')  # Chiqgach login sahifasiga qaytadi


def about_page(request):
    return render(request, 'about.html')


def blog_page(request):
    return render(request, 'blog.html')


def blog_dt_page(request):
    return render(request, 'blog_details.html')


def book_dt_page(request, id):
    book_single = get_object_or_404(Book, id=id)

    context = {
        'book': book_single
    }
    return render(request, 'book-details.html', context=context)


# Savatchani ko‘rish
@login_required(login_url='login')
def cart_page(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)


# Kitob qo‘shish
@login_required(login_url='login')
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{book.title} savatchaga qo‘shildi!")
    return redirect('cart')


# Savatchadan olib tashlash
@login_required(login_url='login')
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.delete()
    messages.success(request, "Kitob savatchadan olib tashlandi!")
    return redirect('cart')


# Checkout Page
@login_required(login_url='login')
def checkout_page(request):
    # Foydalanuvchining savatchasi
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    # Agar savatcha bo‘sh bo‘lsa, checkout sahifasiga ruxsat bermaymiz
    if not cart_items.exists():
        messages.error(request, "Savatchangiz bo‘sh! Avval kitob qo‘shing.")
        return redirect('cart')

    # Buyurtmani tasdiqlash
    if request.method == "POST":
        # Har bir savatchadagi kitob uchun BookOrder yaratamiz
        for item in cart_items:
            BookOrder.objects.create(
                user=request.user,
                book=item.book
            )

        # Savatchani tozalash
        cart_items.delete()

        messages.success(request, "Buyurtmangiz qabul qilindi! Rahmat! ✅")
        return redirect('index')

    context = {
        "cart_items": cart_items,
        "total_price": total_price
    }
    return render(request, "checkout.html", context)


# Payme To‘lov
@login_required(login_url='login')
def payme_checkout(request):
    url = "https://checkout.paycom.uz/api"
    data = {
        "amount": request.user.cart_set.aggregate(Sum('total_price'))['total_price__sum'] * 100,  # Tiynlarda
        "account": {"user_id": request.user.id}
    }
    response = requests.post(url, json=data)
    return JsonResponse(response.json())


# Click To‘lov
@login_required(login_url='login')
def click_checkout(request):
    url = "https://my.click.uz/api"
    data = {
        "amount": request.user.cart_set.aggregate(Sum('total_price'))['total_price__sum'],
        "account": {"user_id": request.user.id}
    }
    response = requests.post(url, json=data)
    return JsonResponse(response.json())


def categories_page(request):
    category_id = request.GET.get('category')  # URL-dan 'category' parametrini olish
    sort_by = request.GET.get('sort')  # URL-dan 'sort' parametrini olish

    categories = Category.objects.all()
    books_list = Book.objects.all()

    # Agar kategoriya tanlangan bo‘lsa, faqat shu kategoriyaga tegishli kitoblarni ko‘rsatamiz
    if category_id:
        books_list = books_list.filter(category_id=category_id)

    # Kitoblarni saralash
    if sort_by:
        if sort_by == 'name':
            books_list = books_list.order_by('title')
        elif sort_by == 'new':
            books_list = books_list.order_by('-publication_year')
        elif sort_by == 'old':
            books_list = books_list.order_by('publication_year')
        elif sort_by == 'price':
            books_list = books_list.order_by('price')

    # Agar category_id mavjud bo‘lsa, raqamga aylantiramiz, aks holda None qo‘yamiz
    selected_category = int(category_id) if category_id and category_id.isdigit() else None

    context = {
        'categories': categories,
        'books_list': books_list,
        'selected_category': selected_category
    }
    return render(request, 'categories.html', context)


def contact_page(request):
    return render(request, 'contact.html')


def elements_page(request):
    return render(request, 'elements.html')

def search_books(request):
    query = request.GET.get('q', '')  # URL-dan qidiruv so‘zini olish
    books_list = Book.objects.all()

    if query:
        books_list = books_list.filter(
            Q(title__icontains=query) | Q(author__icontains=query)  # Kitob nomi yoki muallif bo‘yicha qidirish
        )

    context = {
        'books_list': books_list,
        'query': query  # Qidiruv natijalarini saqlash
    }
    return render(request, 'search_results.html', context)