from rest_framework import generics
from .models import Page, Video, Audio
from .serializers import PageListSerializer, PageSerializer
from django.db.models import F

class PageListView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer

class PageDetailView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    def get(self, request, *args, **kwargs):
        # Атомарно увеличиваем счетчики просмотров
        page = self.get_object()
        content_orders = page.content_orders.all()
        
        for order in content_orders:
            if order.video:
                Video.objects.filter(id=order.video.id).update(counter=F('counter') + 1)
            elif order.audio:
                Audio.objects.filter(id=order.audio.id).update(counter=F('counter') + 1)
        
        return super().retrieve(request, *args, **kwargs)