from rest_framework import serializers
from comm_app.models import *

class AllCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaries
        fields = ('author', 'content', 'creation_date', 'content_type', 'object_id')
