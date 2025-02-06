from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now  # <== BU YERDA TO‘G‘RI IMPORT

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('librarian', 'Kutubxonachi'),
        ('reader', 'Kitob o‘quvchi'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='reader')
    phone = models.CharField(max_length=20, null=True, blank=True)  # Unique olib tashlandi
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username

# Kutubxona filiali
class LibraryBranch(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    librarian = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'librarian'})

    def __str__(self):
        return self.name

# Kitob kategoriyasi
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Kitob modeli
class Book(models.Model):
    FORMAT_CHOICES = (
        ('paper', 'Qog‘oz'),
        ('pdf', 'PDF'),
        ('audio', 'Audiokitob'),
    )

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # To‘g‘rilandi
    library_branch = models.ForeignKey(LibraryBranch, on_delete=models.CASCADE)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='images/book/', null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='paper')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# Kitob ijarasi va tracking
class BookLoan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'reader'})
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    is_damaged = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

# Jarima tizimi
class Fine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_loan = models.OneToOneField(BookLoan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)  # Sana qo‘shildi
    due_date = models.DateTimeField(null=True, blank=True)  # To‘lov muddati qo‘shildi

    def __str__(self):
        return f"{self.user.username} - {self.amount} UZS"

# Online zakaz
class BookOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'reader'})
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    is_picked_up = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'book')  # Bir foydalanuvchi bir kitobni faqat bir marta buyurtma qila oladi

    def __str__(self):
        return f"Order: {self.user.username} - {self.book.title}"

#Cart Modeli
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foydalanuvchi
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Kitob
    quantity = models.PositiveIntegerField(default=1)  # Soni
    added_at = models.DateTimeField(auto_now_add=True)  # Qo‘shilgan vaqt

    def total_price(self):
        return self.quantity * self.book.price  # Jami narx

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.quantity})"