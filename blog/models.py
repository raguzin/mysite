from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset().filter(status='published')
        return queryset

class Post(models.Model):
    """Model definition for Post."""
    STATUS_CHOISE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    # TODO: Define fields here

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOISE, default='draft')

    objects = models.Manager()  # default Manager
    published = PublishedManager()  # new Manager
    tags = TaggableManager()    # taggit manager

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        """Unicode representation of Post."""
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                       self.publish.month, self.publish.day, self.slug])

class Comment(models.Model):
    """Model definition for Comment."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        """Meta definition for Comment."""
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)