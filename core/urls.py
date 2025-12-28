from django.urls import path, include
from .views import register
from .views import LoginView
from rest_framework.routers import DefaultRouter
from .views import (
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


# Namespace for reverse lookups
app_name = "core"

# Register all core viewsets
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
router.register('mentorship', MentorshipRequestViewSet, basename='mentorship')

# Wellbeing endpoints
router.register('moods', MoodViewSet, basename='mood')
router.register('journals', JournalViewSet, basename='journal')
router.register('forum', ForumPostViewSet, basename='forum')

urlpatterns = [
    # All API routes under /api/core/
    path('api/core/', include(router.urls)),
    path('users/update-email/', update_email),
    path('users/change-password/', change_password),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),  
]
