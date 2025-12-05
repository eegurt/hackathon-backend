from django.urls import path
from .views import *


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', VendorLogoutView.as_view(), name='user-logout'),
    path('profile/update/<int:id>/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('change-password/', UserChangePasswordView.as_view(), name='user-change-password'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='user-password-reset'),
    path('<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('', UserListView.as_view(), name='user-list'),
]