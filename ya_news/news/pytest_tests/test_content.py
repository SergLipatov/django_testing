import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count_on_homepage(client, home_url, news_list):
    """Количество новостей на главной странице — ровно 10."""
    assert len(client.get(home_url).context['object_list']) == (
        settings.NEWS_COUNT_ON_HOME_PAGE
    )


def test_news_order(client, home_url):
    """Новости отсортированы по убыванию даты публикации."""
    news_dates = [news.date for news in client.get(home_url).context[
        'object_list']]
    assert news_dates == sorted(news_dates, reverse=True)


def test_comments_order(client, detail_url):
    """Комментарии отображаются в хронологическом порядке."""
    comment_dates = [comment.created for comment in
                     client.get(detail_url).context['news'].comment_set.all()]
    assert comment_dates == sorted(comment_dates)


def test_anonymous_client_has_no_form(client, detail_url):
    """Анонимному пользователю недоступна форма добавления комментариев."""
    assert 'form' not in client.get(detail_url).context


def test_authorized_client_has_form(author_client, detail_url):
    """Для авторизованного пользователя на странице доступна `CommentForm`"""
    assert isinstance(
        author_client.get(detail_url).context.get('form'),
        CommentForm
    )
