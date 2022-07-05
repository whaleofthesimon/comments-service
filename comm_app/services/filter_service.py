from comm_app.models import Comment


def get_queryset_filter(entity_name, object_id, username, start_date, end_date, export):
    if entity_name and object_id:
        if entity_name == 'comment':
            queryset = Comment.objects.filter(id=object_id)
        else:
            queryset = Comment.objects.filter(content_type__model=entity_name, object_id=object_id)
        if export:
            branch_queryset = queryset.get_descendants(include_self=True)
            if start_date and end_date:
                return branch_queryset.filter(creation_date__lte=end_date, creation_date__gte=start_date)
            return branch_queryset
        return queryset

    elif username:
        if start_date and end_date:
            return Comment.objects.filter(author__username=username,
                                          creation_date__lte=end_date,
                                          creation_date__gte=start_date)
        return Comment.objects.filter(author__username=username)

    else:
        return Comment.objects.all()