from django.contrib import admin
from .models import *

admin.site.register(Menu)
admin.site.register(Comment)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Post)
admin.site.register(CommentPost)
admin.site.register(News)
admin.site.register(Category)