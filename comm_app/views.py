from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from comm_app.models import *
from comm_app.serializers import AllCommentsSerializer
from comm_app.services import export_service, filter_service


class CommentsViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    serializer_class = AllCommentsSerializer

    def get_queryset(self, export=False):
        entity_name = self.request.query_params.get('entity')
        object_id = self.request.query_params.get('id')
        username = self.request.query_params.get('username')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        return filter_service.get_queryset_filter(entity_name, object_id, username, start_date, end_date, export)

    def perform_create(self, serializer):  # Autocomplete of "Parent" field by content_type and id
        content_type_id = self.request.data.get('content_type')
        object_id = self.request.data.get('object_id')
        if ContentType.objects.get(id=content_type_id).model == 'comment':
            parent = Comment(pk=object_id)
        else:
            parent = None
        serializer.save(parent=parent)

    @action(detail=False, methods=['get'])
    def branch(self, request):
        branch = self.get_queryset().get_descendants(include_self=True)
        serializer = self.get_serializer(branch, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def csv_export(self, request):
        exporting_queryset = self.get_queryset(export=True)
        return export_service.export_to_csv(exporting_queryset)
