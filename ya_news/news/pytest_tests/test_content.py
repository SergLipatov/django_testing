import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count_on_homepage(client, home_url, news_list):
    """Количество новостей на главной странице — ровно 10."""
    response = client.get(home_url)
    assert len(response.context['object_list']) == (
        settings.NEWS_COUNT_ON_HOME_PAGE
    )


def test_news_order(client, home_url):
    """Новости отсортированы по убыванию даты публикации."""
    response = client.get(home_url)
    assert [news.date for news in response.context['object_list']] == sorted(
        [news.date for news in response.context['object_list']], reverse=True
    )


def test_comments_order(client, detail_url):
    """Комментарии отображаются в хронологическом порядке."""
    response = client.get(detail_url)
    assert [
           comment.created
           for comment in response.context['news'].comment_set.all()
           ] == sorted(
        [
            comment.created
            for comment in response.context['news'].comment_set.all()
        ]
    )


def test_anonymous_client_has_no_form(client, detail_url):
    """Анонимному пользователю недоступна форма добавления комментариев."""
    response = client.get(detail_url)
    assert response.context.get('form') is None


def test_authorized_client_has_form(author_client, detail_url):
    """Для авторизованного пользователя на странице доступна `CommentForm`"""
    response = author_client.get(detail_url)
    assert isinstance(response.context.get('form'), CommentForm)
