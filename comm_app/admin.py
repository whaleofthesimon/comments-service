from django.contrib import admin

from comm_app.models import Commentaries, Posts, Blogs

admin.site.register(Commentaries)
admin.site.register(Posts) #TODO Delete this registration
admin.site.register(Blogs) #TODO Delete this registration
