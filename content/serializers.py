from rest_framework import serializers
from .models import Page, Video, Audio, ContentOrder

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'

class ContentOrderSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    
    def get_content(self, obj):
        if obj.video:
            return VideoSerializer(obj.video).data
        elif obj.audio:
            return AudioSerializer(obj.audio).data
        return None
    
    class Meta:
        model = ContentOrder
        fields = ['content', 'order']

class PageSerializer(serializers.ModelSerializer):
    contents = ContentOrderSerializer(source='content_orders', many=True, read_only=True)
    
    class Meta:
        model = Page
        fields = ['id', 'title', 'contents']

class PageListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='page-detail', format='html')
    
    class Meta:
        model = Page
        fields = ['id', 'title', 'url']