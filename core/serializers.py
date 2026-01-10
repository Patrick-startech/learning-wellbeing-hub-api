from rest_framework import serializers
from django.core import exceptions
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
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
    User,
)

User = get_user_model()


# -------------------------
# User & Library Serializers
# -------------------------

class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'role',
            'date_of_membership',
            'active_status',
            'phone_number',
            'country',
        ]
        read_only_fields = ['id']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'isbn',
            'published_date',
            'copies_available',
            'genre',
            'summary',
            'created_at',
        ]
        read_only_fields = ['created_at','isbn']


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book = serializers.StringRelatedField(read_only=True)
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'id',
            'user',
            'book',
            'checkout_date',
            'due_date',
            'return_date',
            'status',
            'is_overdue',
        ]
        read_only_fields = ['checkout_date', 'due_date', 'return_date', 'is_overdue']

    def get_is_overdue(self, obj):
        return obj.is_overdue()


# -------------------------
# Learning Serializers
# -------------------------

class ResourceSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Resource
        fields = [
            'id',
            'title',
            'description',
            'file_url',
            'created_at',
            'created_by',
        ]
        read_only_fields = ['created_at', 'created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'role',
            'phone_number',
            'country',
        ]

    def validate_password(self, value):
        user = User(
            username=self.initial_data.get('username'),
            email=self.initial_data.get('email'),
        )
        try:
            validate_password(password=value, user=user)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        if hasattr(user, 'is_email_verified'):
            user.is_email_verified = False
        user.save()
        return user


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'correct_answer']


class QuizSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    questions = QuestionSerializer(many=True)
    subject_label = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'created_by',
            'description',
            'subject',
            'subject_label',
            'duration',
            'created_at',
            'questions',
        ]
        read_only_fields = ['created_at', 'created_by']

    def get_subject_label(self, obj):
        return obj.get_subject_display()

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        quiz = Quiz.objects.create(
            created_by=self.context['request'].user,
            **validated_data
        )
        for question in questions_data:
            Question.objects.create(quiz=quiz, **question)
        return quiz


class SubmissionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())

    class Meta:
        model = Submission
        fields = [
            'id',
            'user',
            'quiz',
            'answers',
            'submitted_at',
            'score',
            'percentage',
            'status',
            'feedback',
        ]
        read_only_fields = ['submitted_at', 'score', 'percentage', 'status', 'feedback']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class MentorshipRequestSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    mentor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = MentorshipRequest
        fields = [
            'id',
            'student',
            'mentor',
            'message',
            'status',
            'requested_at',
        ]
        read_only_fields = ['requested_at', 'student', 'status']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['student'] = request.user
        return super().create(validated_data)


class MentorshipRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorshipRequest
        fields = ['status']


# -------------------------
# Wellbeing Serializers
# -------------------------

class MoodSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Mood
        fields = [
            'id',
            'user',
            'mood',
            'logged_at',
        ]
        read_only_fields = ['logged_at', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class JournalSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Journal
        fields = [
            'id',
            'user',
            'created_at',
        ]
        read_only_fields = ['created_at', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ForumPostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ForumPost
        fields = [
            'id',
            'user',
            'title',
            'content',
            'created_at',
            'updated_at',
            'likes',
            'tags',
        ]
        read_only_fields = ['created_at', 'updated_at', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
