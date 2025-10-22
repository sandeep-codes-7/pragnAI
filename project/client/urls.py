from django.urls import path
from . import views

app_name = "client"

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("about/", views.about, name="about"),
    path("Error/", views.Error, name="Error"),
    path("eval/", views.eval_view, name="eval")
]