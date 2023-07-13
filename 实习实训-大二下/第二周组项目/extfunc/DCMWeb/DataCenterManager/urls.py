from django.urls import path

from .views import index, result1, result2, result3, recommend, userSelection


urlpatterns = [
    path("", index),
    path("result1/", result1, name="result1"),
    path("result2/", result2, name="result2"),
    path("result3/", result3, name="result3"),
    path("user-selection/", userSelection, name="user_selection"),
    path("recommend/", recommend, name="recommend"),
]
