from django.contrib import admin
from .models import (
    Book,
    Transaction,
    Resource,
    Quiz,
    Question,
    Submission,
    MentorshipRequest,
    Mood,
    Journal,
    ForumPost,
)

# -------------------------
# Library models
# -------------------------

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "published_date", "copies_available")
    search_fields = ("title", "author", "isbn")
    list_filter = ("published_date",)
    ordering = ("title",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "checkout_date", "due_date", "return_date", "is_overdue")
    list_filter = ("checkout_date", "return_date", "due_date")
    readonly_fields = ("checkout_date", "due_date", "return_date")
    ordering = ("-checkout_date",)


# -------------------------
# Learning models
# -------------------------

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at")
    search_fields = ("title", "description")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "text", "correct_answer")
    search_fields = ("text", "correct_answer")
    ordering = ("quiz",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "score", "submitted_at")
    list_filter = ("score", "submitted_at")
    readonly_fields = ("submitted_at",)
    ordering = ("-submitted_at",)


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    list_display = ("student", "mentor", "status", "requested_at")
    list_filter = ("status", "requested_at")
    readonly_fields = ("requested_at",)
    ordering = ("-requested_at",)


# -------------------------
# Wellbeing models
# -------------------------

@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ("user", "mood", "logged_at")
    list_filter = ("mood", "logged_at")
    readonly_fields = ("logged_at",)
    ordering = ("-logged_at",)


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("entry",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at")
    search_fields = ("title", "content")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
