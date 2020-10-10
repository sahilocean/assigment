from django.conf.urls import url, include
from .views import SignupViews,LoginView,Logout

app_name = "accounts"


urlpatterns = [
	url(r'login/', LoginView.as_view(),name="login"),
	url(r'signup/', SignupViews.as_view(),name="signup"),
	url(r'logout/', Logout.as_view(),name="logout"),
]