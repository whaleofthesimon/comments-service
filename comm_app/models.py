from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Comment(MPTTModel):
    author = models.ForeignKey(User, verbose_name='Автор комментария', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Содержимое комментария')
    creation_date = models.DateField(verbose_name='Дата создания комментария', auto_now_add=True)
    content_type = models.ForeignKey(ContentType, verbose_name='Связанная сущность', on_delete=models.CASCADE,
                                     limit_choices_to={'app_label': 'comm_app'})
    object_id = models.PositiveIntegerField(verbose_name='ID объекта сущности', null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['creation_date']

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Post(models.Model):
    content = models.TextField()


class Blog(models.Model):
    content = models.TextField()
