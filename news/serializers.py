from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    # Use string representation of related fields for readability
    author = serializers.StringRelatedField()
    publisher = serializers.StringRelatedField()

    class Meta:
        model = Article
        # Define fields to be serialized in the API response
        fields = [
            'id',
            'title',
            'content',
            'author',
            'publisher',
            'created_at',
            'approved'  # Add this if you want to expose approval status in API
        ]
