from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from comm_app.models import Comment

admin.site.register(Comment, MPTTModelAdmin)
