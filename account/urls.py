from django.urls import path
from django.contrib.auth import views as auth_views
from . views import (
    SignUp, LogIn, PasswordReset, PasswordResetConfirm,
    activate_user
)


urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('signin/', LogIn.as_view(), name='signin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset-password/', PasswordReset.as_view(), name='reset-password'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('account-activation/<username>/<token>/', activate_user, name="account-activation"),
]
