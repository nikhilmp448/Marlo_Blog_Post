from django.urls import path
from .views import BlogList, PostDetail
from rest_framework.routers import DefaultRouter
from . views import* 

router = DefaultRouter()
## admin nside post crud api
router.register(r'admin', BlogPostViewSet,basename='adminside')
# router.register(r'feedback', FeedbackViewSet,basename='adminside')

urlpatterns = [
    ## user post view List api
    path('posts/', BlogList.as_view(), name='blog-post-list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='blog-post-detail'),
]
urlpatterns += router.urls