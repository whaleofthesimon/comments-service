from rest_framework import serializers
from comm_app.models import *


class AllCommentsSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['content_type'] not in ContentType.objects.all():
            raise serializers.ValidationError("This entity doesn't exist yet!")
        if not data['content_type'].model_class().objects.filter(id=data['object_id']):
            raise serializers.ValidationError("This entity's object doesn't exist yet!")
        return data

    def create(self, validated_data):
        content_type = validated_data.get('content_type')
        object_id = validated_data.get('object_id')
        parent = None
        if content_type.model == 'comment':
            parent = Comment(pk=object_id)
        new_comment = Comment.objects.create(parent=parent, **validated_data)
        return new_comment

    class Meta:
        model = Comment
        fields = (
            'author', 'content', 'creation_date', 'content_type', 'object_id', 'parent', 'level', 'lft', 'rght',
            'tree_id',)
        read_only_fields = ('parent', 'level', 'lft', 'rght', 'tree_id',)
