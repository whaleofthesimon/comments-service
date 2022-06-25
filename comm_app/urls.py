from django.urls import path, include
from rest_framework import routers
from comm_app.views import CommentsViewSet, CommExport

router = routers.SimpleRouter()
router.register(r'commentaries', CommentsViewSet, basename='commentaries')
router.register(r'comm-to-csv', CommExport, basename='comm-to-csv')

urlpatterns = [
    path('', include(router.urls)),

]
