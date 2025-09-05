from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    counter = models.PositiveIntegerField(default=0)
    video_url = models.URLField()
    subtitles_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.title

class Audio(models.Model):
    title = models.CharField(max_length=255)
    counter = models.PositiveIntegerField(default=0)
    text = models.TextField()
    
    def __str__(self):
        return self.title

class Page(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title

class ContentOrder(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='content_orders')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        if self.video:
            return f"{self.page.title} - {self.video.title} (Video)"
        elif self.audio:
            return f"{self.page.title} - {self.audio.title} (Audio)"
        return f"{self.page.title} - Unknown Content"
    
    @property
    def content_type(self):
        if self.video:
            return 'video'
        elif self.audio:
            return 'audio'
        return 'unknown'