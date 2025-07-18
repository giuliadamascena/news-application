from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Article, Newsletter

class Command(BaseCommand):
    help = "Create default user roles and assign permissions"

    def handle(self, *args, **kwargs):
        # Create groups
        reader_group, _ = Group.objects.get_or_create(name='Reader')
        journalist_group, _ = Group.objects.get_or_create(name='Journalist')
        editor_group, _ = Group.objects.get_or_create(name='Editor')

        # Permissions
        article_ct = ContentType.objects.get_for_model(Article)
        newsletter_ct = ContentType.objects.get_for_model(Newsletter)

        # Reader: view only
        view_article = Permission.objects.get(codename='view_article', content_type=article_ct)
        view_newsletter = Permission.objects.get(codename='view_newsletter', content_type=newsletter_ct)
        reader_group.permissions.set([view_article, view_newsletter])

        # Journalist: full permissions
        journalist_perms = Permission.objects.filter(content_type__in=[article_ct, newsletter_ct])
        journalist_group.permissions.set(journalist_perms)

        # Editor: view, change, delete
        editor_perms = Permission.objects.filter(
            content_type__in=[article_ct, newsletter_ct],
            codename__in=[
                'view_article', 'change_article', 'delete_article',
                'view_newsletter', 'change_newsletter', 'delete_newsletter'
            ]
        )
        editor_group.permissions.set(editor_perms)

        self.stdout.write(self.style.SUCCESS("Roles and permissions have been set up."))
