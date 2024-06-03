from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter() # set default router
router.register(r'users', views.userViewSet) # register userViewset and user
router.register(r'recommend', views.recommendResultViewSet)
router.register(r'base-games', views.baseGamesResultViewSet)
router.register(r'steam-games', views.steamGamesResultViewSet)

urlpatterns = [
    path('', include(router.urls))
]