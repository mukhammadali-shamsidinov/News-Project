from django.contrib import admin
from .models import News, Category, Contact, Photography, Comments


# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
  list_display = ['title','slug','published_time','status']
  list_filter = ['status','created_time','published_time']
  prepopulated_fields = {"slug":("title",)}
  date_hierarchy = 'published_time'
  search_fields = ['title','body']
  ordering = ['published_time','status']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['name']

@admin.register(Contact)
class ContactView(admin.ModelAdmin):
  list_display = ['name','email']

@admin.register(Photography)
class PhotoView(admin.ModelAdmin):
  list_display = ['image']

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
  list_display = ['user','body','created_time','active']
  list_filter = ['user','created_time','active']
  search_fields = ['user','body']
  actions = ['disabled_comments','Enabled_commets']

  def disabled_comments(self,request,queryset):
    queryset.update(active=False)
  def Enabled_commets(self,request,queryset):
    queryset.update(active=True)
