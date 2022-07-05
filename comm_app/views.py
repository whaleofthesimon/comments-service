from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters

from comm_app.models import *
from comm_app.serializers import AllCommentsSerializer
from comm_app.services import export_service
from comm_app.services.filter_service import CommonFilter, OnlyCommentFilter, BetweenDateFilter


class CommentsViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    serializer_class = AllCommentsSerializer
    queryset = Comment.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CommonFilter

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get('entity') == 'comment':
            self.filterset_class = OnlyCommentFilter
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs

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
        if self.request.query_params.get('entity') and self.request.query_params.get('id'):
            exporting_queryset = self.get_queryset().get_descendants(include_self=True)
        else:
            exporting_queryset = self.get_queryset()
        exporting_queryset = BetweenDateFilter(self.request.GET, queryset=exporting_queryset).qs
        return export_service.export_to_csv(exporting_queryset)
