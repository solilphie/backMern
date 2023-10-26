from django.urls import path
from django.views.generic import TemplateView

app_name = 'application'

urlpatterns = [
    path('', TemplateView.as_view(template_name="src/index.js")),
]