from django_filters import rest_framework as filters
from comm_app.services.filter_service import OnlyCommentFilter, BetweenDateFilter


class CustomDjangoFilterBackend(filters.DjangoFilterBackend):

    def get_filterset(self, request, queryset, view):
        filterset_class = self.get_filterset_class(view, queryset)
        if filterset_class is None:
            return None
        if request.query_params.get('entity') == 'comment':
            filterset_class = OnlyCommentFilter
        kwargs = self.get_filterset_kwargs(request, queryset, view)
        return filterset_class(**kwargs)

    def date_filter_queryset(self, queryset):
        filterset_class = BetweenDateFilter
        filterset = filterset_class(self.GET, queryset=queryset)
        if filterset is None:
            return queryset
        return filterset.qs
