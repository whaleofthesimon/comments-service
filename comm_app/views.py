from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from comm_app.backends import CustomDjangoFilterBackend
from comm_app.models import *
from comm_app.serializers import AllCommentsSerializer
from comm_app.services import export_service
from comm_app.services.filter_service import CommonFilter


class CommentsViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    serializer_class = AllCommentsSerializer
    queryset = Comment.objects.all()
    filter_backends = (CustomDjangoFilterBackend,)
    filterset_class = CommonFilter

    def get_queryset(self):
        filtered_qs = self.filter_queryset(super().get_queryset())
        if self.action == 'branch' or (self.action == 'csv_export' and
                                       self.request.query_params.get('entity') and
                                       self.request.query_params.get('id')):
            filtered_qs = filtered_qs.get_descendants(include_self=True)
        if self.request.query_params.get('date_after') and self.request.query_params.get('date_after'):
            filtered_qs = self.filter_backends[0].date_filter_queryset(self.request, filtered_qs)
        return filtered_qs

    @action(detail=False, methods=['get'])
    def branch(self, request):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    @action(detail=False, methods=['get'])
    def csv_export(self, request):
        return export_service.export_to_csv(self.get_queryset())
