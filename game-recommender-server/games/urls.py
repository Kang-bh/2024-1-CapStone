from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter() # set default router
router.register(r'users', views.userViewSet) # register userViewset and user
router.register(r'recommend-results', views.recommendResultViewSet)
router.register(r'base-games', views.baseGamesResultViewSet)

urlpatterns = [
    path('', include(router.urls))
]