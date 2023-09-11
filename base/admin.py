from django.contrib import admin
from .models import User,Interest,ConnectionRequest
# Register your models here.

admin.site.register(User)
admin.site.register(Interest)
admin.site.register(ConnectionRequest)


