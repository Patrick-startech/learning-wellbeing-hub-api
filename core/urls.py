from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register,
    LoginView,
    UserViewSet,
    BookViewSet,
    TransactionViewSet,
    ResourceViewSet,
    QuizViewSet,
    SubmissionViewSet,
    MentorshipRequestViewSet,
    MoodViewSet,
    JournalViewSet,
    ForumPostViewSet,
    update_email,
    change_password,
)

app_name = 'core'

# DRF Router
router = DefaultRouter()

# Library endpoints
router.register('users', UserViewSet, basename='user')
router.register('books', BookViewSet, basename='book')
router.register('transactions', TransactionViewSet, basename='transaction')

# Learning endpoints
router.register('resources', ResourceViewSet, basename='resource')
router.register('quizzes', QuizViewSet, basename='quiz')
router.register('submissions', SubmissionViewSet, basename='submission')

# Mentorship endpoints
router.register('mentorshiprequest', MentorshipRequestViewSet, basename='mentorship-request')

# Wellbeing endpoints
router.register('moods', MoodViewSet, basename='mood')
router.register('journals', JournalViewSet, basename='journal')
router.register('forum', ForumPostViewSet, basename='forum')

urlpatterns = [
    path('', include(router.urls)),  # <-- CLEAN: no prefix here
    path('users/update-email/', update_email),
    path('users/change-password/', change_password),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
