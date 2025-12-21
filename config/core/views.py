from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import MeSerializer
from .models import User

from .models import (
    Book, User, Transaction, Resource, Quiz, Question,
    Submission, MentorshipRequest, Mood, Journal, ForumPost
)
from .serializers import (
    UserSerializer, BookSerializer, TransactionSerializer,
    ResourceSerializer, QuizSerializer, QuestionSerializer,
    SubmissionSerializer, MentorshipRequestSerializer,
    MoodSerializer, JournalSerializer, ForumPostSerializer
)
from .permissions import IsAdmin, IsMentorOrAdmin, IsStudent, ReadOnly, IsOwnerOrAdmin

User = get_user_model()


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_email(request):
    user = request.user
    email = request.data.get("email")

    if not email:
        return Response({"detail": "Email is required"}, status=400)

    user.email = email
    user.save()

    return Response(MeSerializer(user).data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    current = request.data.get("current_password")
    new = request.data.get("new_password")

    if not current or not new:
        return Response({"detail": "Both current and new password are required"}, status=400)

    if not user.check_password(current):
        return Response({"detail": "Current password is incorrect"}, status=400)

    user.set_password(new)
    user.save()

    return Response({"detail": "Password updated successfully"})

# -------------------------
# User Management
# -------------------------

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [ReadOnly()]


# -------------------------
# Library Management
# -------------------------

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author', 'isbn']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsMentorOrAdmin()]
        elif self.action == 'destroy':
            return [IsAdmin()]
        elif self.action in ['borrow', 'return_book']:
            return [IsStudent()]
        return [ReadOnly()]

    @action(detail=True, methods=['post'])
    def borrow(self, request):
        book = self.get_object()
        if book.copies_available < 1:
            return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

        if Transaction.objects.filter(user=request.user, book=book, return_date__isnull=True).exists():
            return Response({"error": "You already borrowed this book"}, status=status.HTTP_400_BAD_REQUEST)

        Transaction.objects.create(user=request.user, book=book)
        book.copies_available -= 1
        book.save()
        return Response({"message": f"You borrowed '{book.title}' successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def return_book(self, request):
        book = self.get_object()
        transaction = Transaction.objects.filter(
            user=request.user, book=book, return_date__isnull=True
        ).first()

        if not transaction:
            return Response({"error": "No active borrow found"}, status=status.HTTP_400_BAD_REQUEST)

        transaction.return_date = timezone.now()
        transaction.save()
        book.copies_available += 1
        book.save()
        return Response({"message": f"You returned '{book.title}' successfully"}, status=status.HTTP_200_OK)


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", None) == "admin":
            return Transaction.objects.all()
        return Transaction.objects.filter(user=user)


# -------------------------
# Learning Management
# -------------------------

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsMentorOrAdmin]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsMentorOrAdmin]


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", None) == "admin":
            return Submission.objects.all()
        return Submission.objects.filter(user=user)


class MentorshipRequestViewSet(viewsets.ModelViewSet):
    queryset = MentorshipRequest.objects.all()
    serializer_class = MentorshipRequestSerializer
    permission_classes = [IsStudent]


# -------------------------
# Wellbeing Management
# -------------------------

class MoodViewSet(viewsets.ModelViewSet):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Mood.objects.filter(user=self.request.user)


class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", None) == "admin":
            return Journal.objects.all()
        return Journal.objects.filter(user=user)


class ForumPostViewSet(viewsets.ModelViewSet):
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    permission_classes = [permissions.IsAuthenticated]


def home(request):
    if request.user.is_authenticated:
        return HttpResponse(f"Welcome {request.user.username} to the Learning & Wellbeing Hub API")
    else:
        return HttpResponse("Welcome Guest to the Learning & Wellbeing Hub API")