from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()


class Commentaries(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор комментария', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Содержимое комментария')
    creation_date = models.DateField(verbose_name='Дата создания комментария', auto_now_add=True)
    content_type = models.ForeignKey(ContentType, verbose_name='Связанная сущность', on_delete=models.CASCADE,
                                     limit_choices_to={'app_label': 'comm_app'})
    object_id = models.PositiveIntegerField(verbose_name='ID объекта сущности', null=True) #TODO Add limit by checked type's values count
    related_entity = GenericForeignKey() #TODO Understand purpose of this string or delete it

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

class Posts(models.Model): #TODO Delete after finishing project
    sample_field1 = models.CharField(max_length=64)
    sample_field2 = models.CharField(max_length=64)
    comments = GenericRelation(Commentaries, related_query_name='posts')


class Blogs(models.Model): #TODO Delete after finishing project
    sample_field1 = models.CharField(max_length=64)
    sample_field2 = models.CharField(max_length=64)
    comments = GenericRelation(Commentaries, related_query_name='blogs')



