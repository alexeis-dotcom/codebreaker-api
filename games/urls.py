from rest_framework.routers import SimpleRouter

from .views import GameViewSet

router = SimpleRouter()
router.register("games", GameViewSet, basename="games")

urlpatterns = router.urls
