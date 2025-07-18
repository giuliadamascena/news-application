from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# ───────────────────────────────────────────────
# User Roles
# ───────────────────────────────────────────────

ROLES = (
    ('Reader', 'Reader'),
    ('Journalist', 'Journalist'),
    ('Editor', 'Editor'),
)

# ───────────────────────────────────────────────
# Custom User Model
# ───────────────────────────────────────────────

class User(AbstractUser):
    """
    Extends Django's default user to support roles and subscriptions.
    """
    role = models.CharField(max_length=20, choices=ROLES)

    # Readers can subscribe to journalists
    subscriptions_to_journalists = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='journalist_followers',
        blank=True
    )

    # Readers can subscribe to publishers
    subscriptions_to_publishers = models.ManyToManyField(
        'Publisher',
        related_name='publisher_followers',
        blank=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role:
            group, _ = Group.objects.get_or_create(name=self.role)
            self.groups.clear()
            self.groups.add(group)

    def __str__(self):
        return self.username

# ───────────────────────────────────────────────
# Publisher Model
# ───────────────────────────────────────────────

class Publisher(models.Model):
    """
    Represents a news publisher with associated editors and journalists.
    """
    name = models.CharField(max_length=100, unique=True)
    editors = models.ManyToManyField(User, related_name='editor_of')
    journalists = models.ManyToManyField(User, related_name='journalist_of')

    def __str__(self):
        return self.name

# ───────────────────────────────────────────────
# Article Model
# ───────────────────────────────────────────────

class Article(models.Model):
    """
    Represents a news article submitted by a journalist.

    Attributes:
        title (str): The title of the article.
        content (str): The body content.
        created_at (datetime): Timestamp of creation.
        is_approved (bool): Whether the article is approved by an editor.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# ───────────────────────────────────────────────
# Newsletter Model
# ───────────────────────────────────────────────

class Newsletter(models.Model):
    """
    Represents a newsletter created by a journalist.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    journalist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='newsletters')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.journalist.username}"
