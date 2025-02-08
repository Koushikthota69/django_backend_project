from django.contrib import admin
from .models import Category,Post
class PostAdmin(admin.ModelAdmin):
    list_display=['title','author','category','published_on']
admin.site.register(Category)
admin.site.register(Post,PostAdmin)

# Register your models here.
