from django.core.mail import send_mail
from django.conf import settings
import requests
from .models import User
from django.dispatch import Signal


def send_article_email(article):
    """
    Send an email notification to subscribers about a newly published article.

    The email is sent to:
    - Users who subscribed to the article's publisher.
    - Users who subscribed directly to the journalist (author).

    Args:
        article (Article): The approved article instance that was published.

    Returns:
        None
    """
    subject = f"New Article Published: {article.title}"
    message = f"""
{article.title}
By: {article.author.username}
Published by: {article.publisher.name if article.publisher else 'Independent'}

{article.content}
"""

    # Get subscribers to the publisher
    publisher_subs = User.objects.filter(subscriptions_to_publishers=article.publisher)

    # Get subscribers to the journalist
    journalist_subs = User.objects.filter(subscriptions_to_journalists=article.author)

    # Combine and deduplicate email addresses
    recipient_emails = set(publisher_subs.values_list('email', flat=True)) | \
                       set(journalist_subs.values_list('email', flat=True))

    if recipient_emails:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            list(recipient_emails),
            fail_silently=False
        )


def post_to_x(article):
    """
    Post a summary of the approved article to X (formerly Twitter).

    Constructs a tweet using the article's title, author, and a short preview of the content.
    Posts the tweet using Twitter's API and an access token stored in Django settings.

    Args:
        article (Article): The article to post.

    Returns:
        dict or None: The API response as a dictionary if successful, otherwise None.
    """
    message = f"📰 {article.title} by {article.author.username}!\n\nRead now: {article.content[:100]}..."

    x_api_url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {settings.X_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": message
    }

    try:
        response = requests.post(x_api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error posting to X:", e)
        return None


# Signal to trigger when an article is approved
article_approved_signal = Signal()
