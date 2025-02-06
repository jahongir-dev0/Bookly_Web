from django.urls import path
from .views import *

urlpatterns = [
    path('', index_page, name='index'),
    path('index/', index_page, name='index2'),
    path('about/', about_page, name='about'),
    path('blog/', blog_page, name='blog'),
    path('blog_details/', blog_dt_page, name='blog_details'),
    path('book/<int:id>/', book_dt_page, name='book-details'),
    path('cart/', cart_page, name='cart'),
    path('cart/add/<int:book_id>/', add_to_cart, name='add-to-cart'),
    path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove-from-cart'),
    path('categories/', categories_page, name='categories'),
    path('checkout/', checkout_page, name='checkout'),
    path('contact/', contact_page, name='contact'),
    path('elements/', elements_page, name='elements'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('search/', search_books, name='search-books'),
]
