from django.test import TestCase
from rest_framework.test import APIClient
from news.models import User, Publisher, Article


class ArticleAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test users with different roles
        self.reader = User.objects.create_user(username='reader1', password='pass123', role='Reader')
        self.journalist = User.objects.create_user(username='writer1', password='pass123', role='Journalist')

        # Create a publisher and associate the journalist
        self.publisher = Publisher.objects.create(name='Tech News')
        self.publisher.journalists.add(self.journalist)

        # Subscribe the reader to the publisher (✅ Fix: must be a Publisher, not a User)
        self.reader.subscriptions_to_publishers.add(self.publisher)

        # Create one approved article and one unapproved article
        self.article_approved = Article.objects.create(
            title="Approved Article",
            content="This is an approved article.",
            author=self.journalist,
            publisher=self.publisher,
            approved=True
        )

        self.article_unapproved = Article.objects.create(
            title="Unapproved Article",
            content="This is not approved.",
            author=self.journalist,
            publisher=self.publisher,
            approved=False
        )

        self.reader.subscriptions_to_publishers.add(self.publisher)
        self.reader.subscriptions_to_journalists.add(self.journalist)
        
    def test_reader_can_view_subscribed_articles(self):
        # Log in the test reader
        self.client.login(username='reader1', password='pass123')

        # Send GET request to the articles API endpoint
        response = self.client.get('/api/articles/')

        # Verify the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Only one article should be returned (the approved one)
        self.assertEqual(len(response.data), 1)

        # The article returned should be the approved article
        self.assertEqual(response.data[0]['title'], 'Approved Article')
