from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.utils import timezone
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import MeSerializer
from .models import (
    Book, User, Transaction, Resource, Quiz, Question,
    Submission, MentorshipRequest, Mood, Journal, ForumPost
)
from .serializers import (
    UserSerializer, BookSerializer, TransactionSerializer,
    ResourceSerializer, QuizSerializer, QuestionSerializer,
    SubmissionSerializer, MentorshipRequestSerializer, MentorshipRequestUpdateSerializer,
    MoodSerializer, JournalSerializer, ForumPostSerializer
)
from .permissions import IsAdmin, IsStudent,IsMentorAdminOrReadOnly, ReadOnly, IsOwnerOrAdmin

User = get_user_model()

# -------------------------
# Account Management
# -------------------------

@extend_schema(
    summary='Update user email',
    tags=['Account'],
    examples=[
        OpenApiExample(
            'Example request',
            value={'email': 'newemail@example.com'},
        )
    ],
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_email(request):
    user = request.user
    email = request.data.get('email')

    if not email:
        return Response({'detail': 'Email is required'}, status=400)

    user.email = email
    user.save()

    return Response(MeSerializer(user).data)


@extend_schema(
    summary='Change user password',
    tags=['Account'],
    examples=[
        OpenApiExample(
            'Example request',
            value={
                'current_password': 'oldpass123',
                'new_password': 'newpass456'
            },
        )
    ],
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    current = request.data.get('current_password')
    new = request.data.get('new_password')

    if not current or not new:
        return Response({'detail': 'Both current and new password are required'}, status=400)

    if not user.check_password(current):
        return Response({'detail': 'Current password is incorrect'}, status=400)

    user.set_password(new)
    user.save()

    return Response({'detail': 'Password updated successfully'})


# -------------------------
# Authentication
# -------------------------

@extend_schema(
    summary='Register a new user',
    tags=['Authentication'],
    examples=[
        OpenApiExample(
            'Example registration',
            value={
                'username': 'patrick123',
                'email': 'patrick@example.com',
                'password': 'StrongPass123!',
                'role': 'student',
                'phone_number': '+233501234567',
                'country': 'Ghana'
            },
        )
    ],
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Save user using serializer logic
    user = serializer.save(
        role=request.data.get('role', 'user'),      # default role
        country=request.data.get('country', None),
        phone_number=request.data.get('phone_number', None),
        is_active=True,
        is_staff=False                              # prevent admin access
    )

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)

    return Response(
        {
            'message': 'Registration successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': getattr(user, 'role', None),
                'phone_number': getattr(user, 'phone_number', None),
                'country': getattr(user, 'country', None),
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
        },
        status=status.HTTP_201_CREATED,
    )

@extend_schema(
    summary='Obtain JWT access and refresh tokens',
    tags=['Authentication'],
    examples=[
        OpenApiExample(
            'Example login',
            value={
                'username': 'patrick123',
                'password': 'StrongPass123!'
            },
        )
    ],
)
class LoginView(TokenObtainPairView):
    pass


@extend_schema(
    summary='Refresh JWT access token',
    tags=['Authentication'],
)
class RefreshTokenView(TokenRefreshView):
    pass


# -------------------------
# User Management
# -------------------------

@extend_schema(tags=['Users'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Only admins can create, update, delete users
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'change_role']:
            return [IsAdmin()]
        return [ReadOnly()]

    @action(detail=True, methods=['patch'], url_path='change-role')
    def change_role(self, request, pk=None):
        user = self.get_object()
        new_role = request.data.get("role")

        valid_roles = ["admin", "mentor", "student", "user"]

        if new_role not in valid_roles:
            return Response(
                {"error": "Invalid role. Valid roles: admin, mentor, student, user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.role = new_role
        user.save()

        return Response(
            {"message": "Role updated successfully", "role": user.role},
            status=status.HTTP_200_OK
        )


# -------------------------
# Library Management
# -------------------------

@extend_schema(tags=['Library'])
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author', 'isbn']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsMentorAdminOrReadOnly()]
        if self.action == 'destroy':
            return [IsAdmin()]
        if self.action in ['borrow', 'return_book']:
            return [IsStudent()]
        return [ReadOnly()]

    @extend_schema(summary='Borrow a book', tags=['Library'])
    @action(detail=True, methods=['post'])
    def borrow(self, request):
        book = self.get_object()

        if book.copies_available < 1:
            return Response({'error': 'No copies available'}, status=400)

        if Transaction.objects.filter(user=request.user, book=book, return_date__isnull=True).exists():
            return Response({'error': 'You already borrowed this book'}, status=400)

        Transaction.objects.create(user=request.user, book=book)
        book.copies_available -= 1
        book.save()

        return Response({'message': f'You borrowed {book.title} successfully'})


    @extend_schema(summary='Return a borrowed book', tags=['Library'])
    @action(detail=True, methods=['post'])
    def return_book(self, request):
        book = self.get_object()

        transaction = Transaction.objects.filter(
            user=request.user, book=book, return_date__isnull=True
        ).first()

        if not transaction:
            return Response({'error': 'No active borrow found'}, status=400)

        transaction.return_date = timezone.now()
        transaction.save()

        book.copies_available += 1
        book.save()

        return Response({'message': f'You returned {book.title} successfully'})


@extend_schema(tags=['Library'])
class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'admin':
            return Transaction.objects.all()
        return Transaction.objects.filter(user=user)


# -------------------------
# Learning Management
# -------------------------

@extend_schema(tags=['Resources'])
class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=['Quizzes'],
    summary='Manage quizzes',
    examples=[
        OpenApiExample(
            'Example quiz',
            value={
                'title': 'Basic Algebra',
                'description': 'Test your algebra skills',
                'subject': 'mathematics',
                'duration': 15
            },
        )
    ],
)
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsMentorAdminOrReadOnly]


@extend_schema(tags=['Quizzes'])
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsMentorAdminOrReadOnly]

@extend_schema(tags=['Quizzes'])
class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'admin':
            return Submission.objects.all()
        return Submission.objects.filter(user=user)

    def perform_create(self, serializer):
        submission = serializer.save(user=self.request.user)

        quiz = submission.quiz
        student_answers = submission.answers

        correct = 0
        total = quiz.questions.count()

        for question in quiz.questions.all():
            qid = str(question.id)
            if qid in student_answers and student_answers[qid] == question.correct_answer:
                correct += 1

        # Compute percentage AFTER scoring
        percentage = round((correct / total) * 100) if total > 0 else 0

        # Save score + percentage
        submission.score = correct
        submission.percentage = percentage
        submission.save()

@extend_schema(tags=['Mentorship'])
class MentorshipRequestViewSet(viewsets.ModelViewSet):
    queryset = MentorshipRequest.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return MentorshipRequestUpdateSerializer
        return MentorshipRequestSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


# -------------------------
# Wellbeing Management
# -------------------------

@extend_schema(tags=['Mood'])
class MoodViewSet(viewsets.ModelViewSet):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Mood.objects.filter(user=self.request.user)


@extend_schema(
    tags=['Journal'],
    examples=[
        OpenApiExample(
            'Example journal entry',
            value={'title': 'My day', 'content': 'Today was great'},
        )
    ],
)
class JournalViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'admin':
            return Journal.objects.all()
        return Journal.objects.filter(user=user)


@extend_schema(tags=['Forum'])
class ForumPostViewSet(viewsets.ModelViewSet):
    queryset = ForumPost.objects.all()
    serializer_class = ForumPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer): 
       serializer.save(user=self.request.user)


# -------------------------
# Home & Auth Status
# -------------------------

@api_view(['GET'])
def auth_status(request):
    return Response({
        'is_authenticated': request.user.is_authenticated,
        'user': request.user.username if request.user.is_authenticated else None
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    username = request.user.username if request.user.is_authenticated else None
    return HttpResponse(
        f'Welcome {username} to the Learning & Wellbeing Hub API'
        if username
        else 'Welcome to the Learning & Wellbeing Hub API'
    )

