from django.db import models
import random
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime


# -------------------------
# Helper function for due_date
# -------------------------

def default_due_date():
    '''Default due date is 14 days after checkout.'''
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

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', db_index=True)
    date_of_membership = models.DateField(auto_now_add=True)
    active_status = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.username} ({self.role})'


# -------------------------
# Library Models
# -------------------------

def generate_isbn():
    """Generate a 13‑digit numeric ISBN."""
    return ''.join([str(random.randint(0, 9)) for _ in range(13)])

class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    copies_available = models.PositiveIntegerField(default=1)
    genre = models.CharField(max_length=100, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

    class Meta:
        ordering = ['title']


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    checkout_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=default_due_date)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='borrowed', db_index=True)

    def is_overdue(self):
        return self.return_date is None and timezone.now() > self.due_date

    def __str__(self):
        return f'{self.user.username} borrowed {self.book.title}'

    class Meta:
        ordering = ['-checkout_date']


# -------------------------
# Learning Models
# -------------------------

class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources')

    def __str__(self):
        return self.title


class Quiz(models.Model):
    SUBJECT_CHOICES = [
        ('general', 'General'),
        ('mathematics', 'Mathematics'),
        ('science', 'Science'),
        ('english', 'English'),
        ('biology', 'Biology'),
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('history', 'History'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='general')
    duration = models.IntegerField(default=10, help_text='Duration in minutes')

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quizzes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return f'Q: {self.text[:50]}...'


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.quiz.title} ({self.score})'


class MentorshipRequest(models.Model):
    student = models.ForeignKey(User, related_name='requests', on_delete=models.CASCADE)
    mentor = models.ForeignKey(User, related_name='mentees', on_delete=models.CASCADE)
    message = models.TextField() # <-- NEW FIELD
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending',
        db_index=True,
    )
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.username} → {self.mentor.username} ({self.status})'


# -------------------------
# Wellbeing Models
# -------------------------

class Mood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moods')
    mood = models.CharField(max_length=50, db_index=True)
    logged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.mood}'


class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journals')
    entry = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Journal by {self.user.username} on {self.created_at.date()}'


class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.JSONField(default=list) # Accepts a list of strings
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
