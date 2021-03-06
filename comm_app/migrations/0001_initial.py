# Generated by Django 4.0.4 on 2022-06-23 18:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_field1', models.CharField(max_length=64)),
                ('sample_field2', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_field1', models.CharField(max_length=64)),
                ('sample_field2', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Commentaries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Содержимое комментария')),
                ('creation_date', models.DateField(auto_now_add=True, verbose_name='Дата создания комментария')),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name='ID объекта сущности')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
                ('content_type', models.ForeignKey(limit_choices_to={'app_label': 'comm_app'}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Связанная сущность')),
            ],
        ),
        migrations.AddIndex(
            model_name='commentaries',
            index=models.Index(fields=['content_type', 'object_id'], name='comm_app_co_content_2df6a4_idx'),
        ),
    ]
