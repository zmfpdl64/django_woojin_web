from django.contrib import admin
from .models import Post, Category

admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
   prepopulated_fields = {'slug': ('name', )} #prepopulated_fileds 잘 기입해야지 정상적인 작동이 된다.


admin.site.register(Category, CategoryAdmin)

