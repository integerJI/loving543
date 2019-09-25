from django.contrib import admin
from .models import Memos, Comment, Tag, Tag2

admin.site.register(Memos)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Tag2)

