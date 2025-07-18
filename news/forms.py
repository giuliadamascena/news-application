from django import forms
from .models import Article
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Publisher

class SignUpForm(UserCreationForm):
    ROLE_CHOICES = (
        ('Reader', 'Reader'),
        ('Editor', 'Editor'),
        ('Journalist', 'Journalist'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

class ArticleForm(forms.ModelForm):
    """
    Form for journalists to submit or edit an article.
    """

    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.role == 'Journalist':
            self.fields['publisher'].queryset = user.journalist_of.all()


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name']