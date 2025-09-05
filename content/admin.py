from django.contrib import admin
from .models import Page, Video, Audio, ContentOrder

class ContentOrderInline(admin.TabularInline):
    model = ContentOrder
    extra = 1
    fields = ['get_content_type', 'video', 'audio', 'order']
    readonly_fields = ['get_content_type']
    
    def get_content_type(self, obj):
        return obj.content_type
    get_content_type.short_description = 'Content Type'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "video":
            kwargs["queryset"] = Video.objects.all()
        elif db_field.name == "audio":
            kwargs["queryset"] = Audio.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [ContentOrderInline]
    list_display = ['title']
    search_fields = ['title__istartswith']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_url']
    search_fields = ['title__istartswith']

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ['title', 'text_preview']
    search_fields = ['title__istartswith']
    
    def text_preview(self, obj):
        if obj.text and len(obj.text) > 50:
            return f"{obj.text[:50]}..."
        return obj.text
    text_preview.short_description = 'Text Preview'

@admin.register(ContentOrder)
class ContentOrderAdmin(admin.ModelAdmin):
    list_display = ['page', 'get_content_type', 'get_content_title', 'order']
    list_filter = ['page']
    
    def get_content_type(self, obj):
        return obj.content_type
    get_content_type.short_description = 'Content Type'
    
    def get_content_title(self, obj):
        if obj.video:
            return obj.video.title
        elif obj.audio:
            return obj.audio.title
        return "No content"
    get_content_title.short_description = 'Content Title'