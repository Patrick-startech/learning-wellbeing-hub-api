from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
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

User = get_user_model()

# -------------------------
# Library models
# -------------------------

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "isbn",
        "published_date",
        "copies_available",
        "genre",
    )
    search_fields = ("title", "author", "isbn", "genre")
    list_filter = ("published_date", "genre")
    ordering = ("title",)


@admin.action(description="Mark selected transactions as returned")
def mark_as_returned(modeladmin, request, queryset):
    user = request.user
    for transaction in queryset.filter(return_date__isnull=True):
        transaction.return_date = timezone.now()
        transaction.status = "returned"
        transaction.book.copies_available += 1
        transaction.book.save()
        transaction.save()
    modeladmin.message_user(
        request,
        f"{queryset.count()} transactions marked as returned by {user}."
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "book",
        "checkout_date",
        "due_date",
        "return_date",
        "status",
        "is_overdue",
    )
    list_filter = ("status", "checkout_date", "return_date", "due_date")
    readonly_fields = ("checkout_date", "due_date", "return_date")
    ordering = ("-checkout_date",)
    actions = [mark_as_returned]


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


@admin.action(description="Approve selected mentorship requests")
def approve_requests(modeladmin, request, queryset):
    queryset.update(status="approved")


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    list_display = ("student", "mentor", "status", "requested_at")
    list_filter = ("status", "requested_at")
    readonly_fields = ("requested_at",)
    ordering = ("-requested_at",)
    actions = [approve_requests]


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
    list_display = ("title", "user", "created_at", "updated_at", "likes")
    search_fields = ("title", "content")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


# -------------------------
# Custom User Model
# -------------------------

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_superuser", "active_status")
    list_filter = ("role", "is_staff", "is_superuser", "active_status")
    search_fields = ("username", "email")

    fieldsets = UserAdmin.fieldsets + (
        ("Role & Status", {"fields": ("role", "active_status")}),
    )
