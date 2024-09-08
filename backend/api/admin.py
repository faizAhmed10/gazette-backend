from django.contrib import admin
from api.models import *
from mptt.admin import MPTTModelAdmin
# Register your models here.

admin.site.register(Authors)
admin.site.register(AllowAuthor)
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Comment, MPTTModelAdmin)