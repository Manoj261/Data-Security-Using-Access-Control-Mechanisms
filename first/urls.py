"""
URL configuration for first project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from first import settings
from .views import home
from .views import login
from . import settings
from .views import cheap
from .views import signup
from .views import sendmail
from .views import verify_otp
from .views import signin
from .views import lvf
from .views import predict
from .views import resend_otp
from .views import model
from .views import message_testing
from .views import submit
from .views import hot
from .views import profile
from .views import predictions
from .views import logout_view_secc
from .views import sample_text
from .views import delete_user
from .views import admin1
urlpatterns = [
    path('send/',sendmail),
    path("admin1/",admin1,name="admin1"),
    path('',home),
    path('loginotp/',login),
    path('home/',cheap),
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    #path('manage_users/',manage_users, name='manage_users'),
    path('signin/',signin,name='signin'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('db/abc/verification_success',lvf,name='lvf'),
    path('predict/',predict,name='predict'),
    path('profile/',profile,name="profile"),
    path('model/',model,name='model'),
    path('resend_otp/',resend_otp,name="resend_otp"),
    path('ass/',message_testing,name="msg_test"),
    path('submit/',submit,name="submit"),
    path('hot/',hot,name="hot"),
    path('logout/',logout_view_secc,name='logout'),
    path("predictions/",predictions,name="predictions"),
    path("sample_text/",sample_text,name="sample_text"),
    path("delete_user/<str:username>",delete_user,name="delete_user"
    )
]
