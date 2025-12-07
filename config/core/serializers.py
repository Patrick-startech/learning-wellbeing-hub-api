from rest_framework import serializers
from django.contrib.auth import get_user_model
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
# User & Library Serializers
# -------------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'date_of_membership', 'active_status']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'copies_available']


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'book', 'checkout_date', 'due_date', 'return_date', 'is_overdue']
        read_only_fields = ['checkout_date', 'due_date', 'return_date', 'is_overdue']


# -------------------------
# Learning Serializers
# -------------------------

class ResourceSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Resource
        fields = ['id', 'title', 'description', 'file_url', 'created_at', 'created_by']
        read_only_fields = ['created_at', 'created_by']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'correct_answer']


class QuizSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'created_by', 'created_at', 'questions']
        read_only_fields = ['created_at', 'created_by']


class SubmissionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    quiz = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'user', 'quiz', 'submitted_at', 'score']
        read_only_fields = ['submitted_at', 'score']


class MentorshipRequestSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    mentor = serializers.StringRelatedField()

    class Meta:
        model = MentorshipRequest
        fields = ['id', 'student', 'mentor', 'status', 'requested_at']
        read_only_fields = ['requested_at', 'student']


# -------------------------
# Wellbeing Serializers
# -------------------------

class MoodSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Mood
        fields = ['id', 'user', 'mood', 'logged_at']
        read_only_fields = ['logged_at', 'user']


class JournalSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Journal
        fields = ['id', 'user', 'entry', 'created_at']
        read_only_fields = ['created_at', 'user']


class ForumPostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ForumPost
        fields = ['id', 'user', 'title', 'content', 'created_at']
        read_only_fields = ['created_at', 'user']
