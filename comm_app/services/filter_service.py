from comm_app.models import Comment
from django_filters import rest_framework as filters


class CommonFilter(filters.FilterSet):
    entity = filters.CharFilter(field_name='content_type__model')
    id = filters.NumberFilter(field_name='object_id')
    username = filters.CharFilter(field_name='author__username')

    class Meta:
        model = Comment
        fields = ['author__username', 'content_type__model', 'object_id']


class OnlyCommentFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id')

    class Meta:
        model = Comment
        fields = ['id']


class BetweenDateFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter(field_name='creation_date')

    class Meta:
        model = Comment
        fields = ['creation_date']
