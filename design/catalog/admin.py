from django.contrib import admin
from .models import *

# admin.site.register(Application)
admin.site.register(Category)
admin.site.register(AuthUser)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status')
