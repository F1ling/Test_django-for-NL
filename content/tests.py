from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Page, Video, Audio, ContentOrder

class PageAPITests(APITestCase):
    def setUp(self):
        self.page = Page.objects.create(title="Test Page")
        self.video = Video.objects.create(title="Test Video", video_url="http://example.com/video.mp4")
        self.audio = Audio.objects.create(title="Test Audio", text="Some text")
        ContentOrder.objects.create(page=self.page, content=self.video, order=0)
        ContentOrder.objects.create(page=self.page, content=self.audio, order=1)

    def test_page_list(self):
        url = reverse('page-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_page_detail(self):
        url = reverse('page-detail', kwargs={'pk': self.page.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['contents']), 2)