from django.urls import path
from .views import resgister_user,login_user,logout_user


urlpatterns = [
					path("signup/",resgister_user,name="signup"),
					path("login/",login_user,name="login"),
					path("logout/",logout_user,name="logout"),

]