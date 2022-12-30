from django.urls import path
from DomeApp.views import *

app_name = "dome"

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
]
