"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
from django.contrib import admin
from core.views import home
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Import your viewsets from the core app
from core.views import (
    UserViewSet,
    BookViewSet,
    TransactionViewSet,
    # Add these only once they exist in core/views.py
    # ResourceViewSet,
    # QuizViewSet,
    # SubmissionViewSet,
    # MoodViewSet,
    # JournalViewSet,
    # ForumPostViewSet,
    # MentorshipRequestViewSet,
)

# Register API routes
router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('books', BookViewSet, basename='book')
router.register('transactions', TransactionViewSet, basename='transaction')

# Uncomment these once the viewsets are implemented
# router.register('resources', ResourceViewSet, basename='resource')
# router.register('quizzes', QuizViewSet, basename='quiz')
# router.register('submissions', SubmissionViewSet, basename='submission')
# router.register('moods', MoodViewSet, basename='mood')
# router.register('journals', JournalViewSet, basename='journal')
# router.register('forum', ForumPostViewSet, basename='forum')
# router.register('mentorship', MentorshipRequestViewSet, basename='mentorship')

urlpatterns = [
    path('', home, name='home'),   # ✅ now / will work
    # Admin panel
    path('admin/', admin.site.urls),

    # Authentication endpoints (JWT)
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Core app endpoints
    path('api/', include(router.urls)),

    path('', include('core.urls')),
]
