from rest_framework.routers import DefaultRouter
from .views import ProjectsViewSet

router = DefaultRouter()
router.register(r'projects', ProjectsViewSet, basename='projects')

urlpatterns = router.urls
