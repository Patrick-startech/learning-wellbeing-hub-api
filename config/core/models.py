from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime


# -------------------------
# Helper function for due_date
# -------------------------

def default_due_date():
    """Default due date is 14 days after checkout."""
    return timezone.now() + datetime.timedelta(days=14)


# -------------------------
# Custom User Model
# -------------------------

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('mentor', 'Mentor'),
        ('student', 'Student'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    date_of_membership = models.DateField(auto_now_add=True)
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return self.username


# -------------------------
# Library Models
# -------------------------

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    copies_available = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    checkout_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=default_due_date)  # ✅ fixed
    return_date = models.DateTimeField(null=True, blank=True)

    def is_overdue(self):
        return self.return_date is None and timezone.now() > self.due_date

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"


# -------------------------
# Learning Models
# -------------------------

class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return f"Q: {self.text[:50]}..."


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score})"


class MentorshipRequest(models.Model):
    student = models.ForeignKey(User, related_name="requests", on_delete=models.CASCADE)
    mentor = models.ForeignKey(User, related_name="mentees", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")],
        default="pending",
    )
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} → {self.mentor.username} ({self.status})"


# -------------------------
# Wellbeing Models
# -------------------------

class Mood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=50)  # e.g., "happy", "stressed"
    logged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood}"


class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Journal by {self.user.username} on {self.created_at.date()}"


class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
