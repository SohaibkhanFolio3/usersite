
from directory import views
from rest_framework.routers import DefaultRouter
from django.urls import path , include

router = DefaultRouter()
router.register('First-viewset', views.HelloViewSet , basename='first-viewset')
Userrouter = DefaultRouter()
Userrouter.register('User-Profile' , views.UserprofileViewSet, basename='user-profile' )


urlpatterns = [
    path("hello/", views.HelloApiView.as_view(), name='Api1' ),
    path('login/', views.UserLoginApiView.as_view() , name='login'),
    path("", include(router.urls)),
    path("users/", include(Userrouter.urls))
    
]

