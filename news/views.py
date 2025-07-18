from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseForbidden
from django.views import View
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Article, Publisher, User
from .forms import ArticleForm, SignUpForm, PublisherForm
from .utils import post_to_x
from .serializers import ArticleSerializer
from .signals import article_approved_signal

# ────────────────────────────────
# Public Homepage
# ────────────────────────────────

def home(request):
    """Render the homepage."""
    return render(request, 'news/home.html')


# ────────────────────────────────
# Dashboard & Articles (Web Views)
# ────────────────────────────────

@login_required
def dashboard(request):
    """Show user dashboard based on role."""
    user = request.user
    if user.role == 'Editor':
        articles = Article.objects.filter(publisher__editors=user)
    elif user.role == 'Journalist':
        articles = Article.objects.filter(author=user)
    else:  # Reader
        articles = Article.objects.filter(approved=True)
    return render(request, 'news/dashboard.html', {'articles': articles})


def article_list(request):
    """
    Display a list of all approved articles.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Rendered template with the list of approved articles.
    """
    articles = Article.objects.filter(is_approved=True)
    return render(request, 'news/article_list.html', {'articles': articles})



def article_detail(request, pk):
    """Display a specific approved article."""
    article = get_object_or_404(Article, pk=pk, approved=True)
    return render(request, 'news/article_detail.html', {'article': article})


@method_decorator(login_required, name='dispatch')
class ArticleCreateView(View):
    """View for journalists to create new articles."""
    def get(self, request):
        if request.user.role != 'Journalist':
            return HttpResponseForbidden()
        form = ArticleForm(user=request.user)
        return render(request, 'news/article_form.html', {'form': form})

    def post(self, request):
        if request.user.role != 'Journalist':
            return HttpResponseForbidden()
        form = ArticleForm(request.POST, user=request.user)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "Article submitted for review.")
            return redirect('dashboard')
        return render(request, 'news/article_form.html', {'form': form})


# ────────────────────────────────
# Editor-Only Views
# ────────────────────────────────

def is_editor(user):
    """Check if the user is an editor."""
    return user.role == 'Editor'


@login_required
@user_passes_test(is_editor)
def pending_articles(request):
    """Show articles awaiting approval."""
    articles = Article.objects.filter(approved=False)
    return render(request, 'editor/approve_articles.html', {'articles': articles})


@login_required
@user_passes_test(is_editor)
def approve_article(request, article_id):
    """Approve an article, send emails, and post to X."""
    article = get_object_or_404(Article, id=article_id)

    if article.approved:
        messages.info(request, "Article already approved.")
        return redirect('pending_articles')

    article.approved = True
    article.save()

    # Notify all subscribers (journalist or publisher)
    subscribers = User.objects.filter(role='Reader').filter(
        subscriptions_to_journalists=article.author
    ) | User.objects.filter(
        subscriptions_to_publishers=article.publisher
    )

    subject = f"New Article Approved: {article.title}"
    message = f"{article.content}\n\nBy {article.author.get_full_name()}"

    for subscriber in subscribers.distinct():
        send_mail(subject, message, settings.EMAIL_HOST_USER, [subscriber.email])

    # Post to X (Twitter)
    try:
        post_to_x(article)
    except Exception as e:
        print("Error posting to X:", e)

    # Trigger custom signal
    article_approved_signal.send(sender=Article, instance=article)

    messages.success(request, "Article approved and shared.")
    return redirect('pending_articles')


# ────────────────────────────────
# REST API Views
# ────────────────────────────────

class ArticleListAPI(APIView):
    """API: List articles; filter by reader subscriptions."""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user = request.user
        if user.is_authenticated and user.role == 'Reader':
            subscriptions_to_journalists = user.subscriptions_to_journalists.all()
            subscriptions_to_publishers = user.subscriptions_to_publishers.all()

            articles = Article.objects.filter(approved=True).filter(
                author__in=subscriptions_to_journalists
            ) | Article.objects.filter(
                approved=True, publisher__in=subscriptions_to_publishers
            )
        else:
            articles = Article.objects.filter(approved=True)

        serializer = ArticleSerializer(articles.distinct(), many=True)
        return Response(serializer.data)


class ArticleDetailAPI(APIView):
    """API: Retrieve details for a single approved article."""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk, approved=True)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


# ────────────────────────────────
# User Signup View
# ────────────────────────────────

class SignUpView(CreateView):
    """Allow users to register and auto-login."""
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('homepage')


# ────────────────────────────────
# Publisher Creation View (Editor only)
# ────────────────────────────────

@login_required
@require_http_methods(["GET", "POST"])
def create_publisher(request):
    """Allow Editors to create a new Publisher."""
    if request.user.role != 'Editor':
        return HttpResponseForbidden()

    if request.method == "POST":
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save()
            messages.success(request, f"Publisher '{publisher.name}' created successfully.")
            return redirect("dashboard")
    else:
        form = PublisherForm()

    return render(request, "news/create_publisher.html", {"form": form})
