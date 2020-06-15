from django.contrib import admin
from .models import Search,Login,Post,Signup

# Register your models here.
admin.site.register(Search)
admin.site.register(Login)
admin.site.register(Post)
admin.site.register(Signup)