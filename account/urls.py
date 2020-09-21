from django.urls import path, include
from account.views import auth_view
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
	path('auth', auth_view),
	#path('', include('django.contrib.auth.urls')),
]