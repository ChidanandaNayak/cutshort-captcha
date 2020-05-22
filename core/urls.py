
from django.urls import path
from .views import GenerateCaptchaView
from django.conf import settings
from django.conf.urls.static import static
app_name = 'core'

urlpatterns = [
    path('',GenerateCaptchaView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)