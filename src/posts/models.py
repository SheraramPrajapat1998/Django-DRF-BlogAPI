from django.db import models

from django.utils import timezone
from django.conf import settings

class Post(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    image = models.ImageField(upload_to='blog/posts', blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default=DRAFT, max_length=10)
    publish = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title', '-created_at', )
    
    def __str__(self):
        return self.title
