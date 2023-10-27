
from .views import UserRegisterViewset
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import*

router = DefaultRouter()

router.register(r'register',UserRegisterViewset,basename='register')

urlpatterns = [
    ## retrieve delete update my account 
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]

urlpatterns+= router.urls