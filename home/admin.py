from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, LibraryBranch, Category, Book, BookLoan, Fine, BookOrder

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'role', 'phone', 'address', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'phone', 'address')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Shaxsiy ma’lumotlar', {'fields': ('role', 'phone', 'address')}),
        ('Ruxsatlar', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Muqaddas sanalar', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(LibraryBranch)
class LibraryBranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'librarian')
    search_fields = ('name', 'location')
    list_filter = ('librarian',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'library_branch', 'total_copies', 'available_copies',
                    'isbn', 'publication_year', 'language', 'format', 'price', 'added_date', 'image')
    list_filter = ('category', 'library_branch', 'publication_year', 'language', 'format')
    search_fields = ('title', 'author', 'isbn')
    list_editable = ('available_copies', 'price')

@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'issue_date', 'due_date', 'return_date', 'is_damaged')
    list_filter = ('issue_date', 'due_date', 'return_date', 'is_damaged')
    search_fields = ('user__username', 'book__title')

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_loan', 'amount', 'is_paid')
    list_filter = ('is_paid',)
    search_fields = ('user__username', 'book_loan__book__title')

@admin.register(BookOrder)
class BookOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'order_date', 'is_picked_up')
    list_filter = ('is_picked_up', 'order_date')
    search_fields = ('user__username', 'book__title')