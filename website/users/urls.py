from django.urls import include, path
from users.views import UsersDetailView


app_name = "users"
urlpatterns = [path("<int:pk>/", UsersDetailView.as_view(), name="detail")]
