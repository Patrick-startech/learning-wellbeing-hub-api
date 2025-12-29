from django.test import TestCase
from django.utils import timezone
from .models import User, Book, Transaction

class TransactionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="student1", role="student")
        self.book = Book.objects.create(title="Test Book", author="Author", isbn="1234567890123", published_date="2025-01-01", copies_available=1)

    def test_borrow_and_return(self):
        transaction = Transaction.objects.create(user=self.user, book=self.book)
        self.assertFalse(transaction.is_overdue())
        transaction.return_date = timezone.now()
        transaction.save()
        self.assertIsNotNone(transaction.return_date)
