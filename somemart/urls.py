from django.urls import path

from .views import AddItemView

urlpatterns = [
    path('api/v1/goods/', AddItemView.as_view()),
]
