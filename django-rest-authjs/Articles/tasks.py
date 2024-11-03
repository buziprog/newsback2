from celery import shared_task
from django.db import models  # Import models if you haven't already
import pytz
from datetime import datetime
import requests

# Import Articles if you haven't already
from .models import Articles
# Import ArticleSerializer if you haven't already

# Your other imports here, like models, datetime, etc.


@shared_task
def fetch_and_store_articles():
    # Delete all existing articles
    Articles.objects.all().delete()

    response = requests.get('https://opinion.al/wp-json/wp/v2/posts')
    print("Response Status:", response.status_code)

    if response.status_code == 200:
        articles = response.json()

        for article in articles:
            wp_featuredmedia = article.get(
                '_links', {}).get('wp:featuredmedia', [])
            medium_image_url = ''

            for media_item in wp_featuredmedia:
                if 'href' in media_item:
                    media_response = requests.get(media_item['href'])
                    if media_response.status_code == 200:
                        media_data = media_response.json()
                        medium_image_url = media_data.get('source_url', '')
                    break

            wp_term = article.get('_links', {}).get('wp:term', [])
            category_names = []

            naive_datetime = datetime.fromisoformat(article['date_gmt'])
            aware_datetime = pytz.utc.localize(naive_datetime)

            Articles.objects.create(
                title=article['title']['rendered'],
                content=article['content']['rendered'],
                slug=article['slug'],
                published_at=aware_datetime,
                image_url=medium_image_url,


            )
