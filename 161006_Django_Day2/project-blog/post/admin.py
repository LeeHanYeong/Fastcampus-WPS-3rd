from django.contrib import admin
# 현재위치 기준으로 models라는 모듈에서 Post클래스를 import해온다
from .models import Post

# Django admin사이트에 Post모델을 등록한다
admin.site.register(Post)




# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'description', 'created', )

# admin.site.register(Post, PostAdmin)