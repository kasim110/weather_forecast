from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path("user-register/",views.UserRegisterView.as_view(),name='user-register'),
    path("user-login/",views.UserLoginView.as_view(),name="user-login"),
    path("user-logout/",views.UserLogout.as_view(),name="user-logout"),
    path("get-history-weather-data/",views.HistoricWeatherAPIView.as_view(),name="weather-data")
]