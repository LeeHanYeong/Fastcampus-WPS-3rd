from django.contrib import admin
from .models import *


admin.site.register(Photo)
admin.site.register(PhotoLike)
admin.site.register(PhotoComment)
admin.site.register(PhotoTag)
