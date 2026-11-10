from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path("new/", views.create_document_view, name="create"),
    path("track/<str:tracking_number>/", views.tracker_view, name="track"),
]