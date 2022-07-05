import csv

from django.http import HttpResponse


def export_to_csv(exporting_queryset):
    output = []
    response = HttpResponse(content_type='text/csv')
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['Author', 'Content', 'Creation Date', 'Related Entity', 'Object ID'])
    for comment in exporting_queryset:
        output.append([comment.author,
                       comment.content,
                       comment.creation_date,
                       comment.content_type.model,
                       comment.object_id])
    writer.writerows(output)
    return response
