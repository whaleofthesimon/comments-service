import csv

from django.http import HttpResponse
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from comm_app.models import *
from comm_app.serializers import AllCommentsSerializer


class CommentsViewSet(mixins.CreateModelMixin,
                      GenericViewSet):
    serializer_class = AllCommentsSerializer
    queryset = Commentaries.objects.all()

    @action(detail=False, methods=['get'], url_path=r'comm_for_entity/(?P<entity_name>\w+)/(?P<object_id>\w+)')
    def comm_for_entity(self, request, entity_name, object_id):
        comm_list = Commentaries.objects.filter(content_type__model=entity_name, object_id=object_id)
        paged_comm_list = self.paginate_queryset(comm_list)
        if paged_comm_list is not None:
            serializer = self.get_serializer(paged_comm_list, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(comm_list, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'comm_branch/(?P<entity_name>\w+)/(?P<object_id>\w+)')
    def comm_branch(self, request, entity_name, object_id):
        comm_list = []

        def get_comm_list(entity_name, object_id):
            query_request = Commentaries.objects.filter(content_type__model=entity_name, object_id=object_id)
            if query_request:
                comm_list.extend(list(query_request))
            for query in query_request:
                get_comm_list(entity_name='commentaries', object_id=query.id)

        get_comm_list(entity_name, object_id)
        serializer = self.get_serializer(comm_list, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'comm_by_user/(?P<username>\w+)')
    def comm_by_user(self, request, username):
        comm_list = Commentaries.objects.filter(author__username=username)
        serializer = self.get_serializer(comm_list, many=True)
        return Response(serializer.data)


class CommExport(GenericViewSet):

    @staticmethod
    def get_csv(query_set):
        output = []
        response = HttpResponse(content_type='text/csv')
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        writer.writerow(['Author', 'Content', 'Creation Date', 'Related Entity', 'Object ID'])
        for comment in query_set:
            output.append([comment.author,
                           comment.content,
                           comment.creation_date,
                           comment.content_type.model,
                           comment.object_id])
        writer.writerows(output)
        return response

    @action(detail=False, url_path=r'get_csv/(?P<username>\w+)'
                                   r'(/(?P<start_date>[\w-]+)/(?P<end_date>[\w-]+))*')
    def get_csv_by_user(self, request, username, start_date=None, end_date=None):
        if start_date and end_date:
            query_set = Commentaries.objects.filter(author__username=username,
                                                    creation_date__lte=end_date,
                                                    creation_date__gte=start_date)
        else:
            query_set = Commentaries.objects.filter(author__username=username)
        return CommExport.get_csv(query_set)

    @action(detail=False, url_path=r'get_csv/(?P<entity_name>\w+)/(?P<object_id>\w+)'
                                   r'(/(?P<start_date>[\w-]+)/(?P<end_date>[\w-]+))*')
    def get_csv_by_entity(self, request, entity_name, object_id, start_date=None, end_date=None):
        query_set = []

        def get_query_set(entity_name, object_id):
            if start_date and end_date:
                query_request = Commentaries.objects.filter(content_type__model=entity_name,
                                                            object_id=object_id,
                                                            creation_date__lte=end_date,
                                                            creation_date__gte=start_date)
            else:
                query_request = Commentaries.objects.filter(content_type__model=entity_name,
                                                            object_id=object_id)
            if query_request:
                query_set.extend(list(query_request))
            for query in query_request:
                get_query_set(entity_name='commentaries', object_id=query.id)

        get_query_set(entity_name, object_id)
        return CommExport.get_csv(query_set)
