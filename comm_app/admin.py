from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from comm_app.models import Comment, Post, Blog

admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(Post)
admin.site.register(Blog)
