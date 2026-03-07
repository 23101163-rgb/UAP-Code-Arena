from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),  # Login page URL
    path("signup/", views.signup_view, name="signup"),  # Signup page URL
    path("logout/", views.logout_view, name="logout"),  # Logout URL
    path("", views.home_view, name="home"),  # Home page at the root
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)