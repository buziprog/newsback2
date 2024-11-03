from django.db import models


class Articles(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField()
    published_at = models.DateTimeField()
    image_url = models.URLField()
    link = models.URLField()

    class Meta:
        app_label = 'Articles'
    # add any other fields you want
