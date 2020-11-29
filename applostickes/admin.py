from django.contrib import admin

# Register your models here.

from .models import User, UserGroup, Transaction, Element

admin.site.register(User)
admin.site.register(UserGroup)
admin.site.register(Transaction)
admin.site.register(Element)