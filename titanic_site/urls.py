from django.urls import path
from predictor.views import home, predict

urlpatterns = [
    path("", home, name="home"),
    path("predict/", predict, name="predict"),
]
