from django.urls import path, include
from rest_framework import routers
from comm_app.views import CommentsViewSet

router = routers.SimpleRouter()
router.register(r'commentaries', CommentsViewSet, basename='commentaries')

urlpatterns = [
    path('', include(router.urls)),

]

