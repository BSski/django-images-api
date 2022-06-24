from django.urls import path

from users.views import UsersDetailView


app_name = "users"
urlpatterns = [
    path("<int:pk>/", UsersDetailView.as_view(), name="detail")
]
