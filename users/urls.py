from xml.etree.ElementInclude import include
from django import views
from django.urls import path, include
from rest_framework import routers
from users import views

router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet)

urlpatterns = [
    path('me', views.SelfMethods.as_view()),
    path('', include(router.urls))
]
