from django.contrib import admin
from .models import Event, Category, SubCategory
# Register your models here.


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'area','image']


admin.site.register(Event, EventAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'team_head_name', 'team_head_mobile']


admin.site.register(Category, CategoryAdmin)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']


admin.site.register(SubCategory, SubCategoryAdmin)