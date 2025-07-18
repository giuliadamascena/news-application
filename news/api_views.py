from rest_framework import generics, permissions
from .models import Article
from .serializers import ArticleSerializer

class ArticleListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Article.objects.filter(
            approved=True
        ).filter(
            publisher__in=user.subscriptions_to_publishers.all()
        ) | Article.objects.filter(
            approved=True,
            author__in=user.subscriptions_to_journalists.all()
        )

class ArticleDetailAPIView(generics.RetrieveAPIView):
    queryset = Article.objects.filter(approved=True)
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
