from django.urls import path
from . import views

urlpatterns = [
    path("", views.feedback_list, name="feedback_list"),
    path("new/", views.feedback_new_post, name="feedback_new_post"),
    path("<int:pk>/", views.FeedbackDetailView.as_view(), name="feedback_detail"),
]
