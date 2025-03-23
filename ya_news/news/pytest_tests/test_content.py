from django.conf import settings
from django.urls import reverse


def test_news_count_on_homepage(client, create_news):
    """Количество новостей на главной странице — не более 10."""
    url = reverse('news:home')
    response = client.get(url)

    assert len(
        response.context['news_feed']) <= settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, create_news):
    """Новости отсортированы от самой свежей к самой старой."""
    url = reverse('news:home')
    response = client.get(url)

    news_feed = response.context['news_feed']
    news_dates = [news.date for news in news_feed]

    assert news_dates == sorted(news_dates, reverse=True)


def test_comments_order(client, news, create_comments):
    """Комментарии отсортированы в хронологическом порядке."""
    url = reverse('news:detail', args=[news.pk])
    response = client.get(url)

    comments = response.context['news'].comment_set.all()
    comment_times = [comment.created for comment in comments]

    assert comment_times == sorted(comment_times)


def test_anonymous_client_has_no_form(client, news):
    """Анонимному пользователю недоступна форма для отправки комментария."""
    url = reverse('news:detail', args=[news.pk])
    response = client.get(url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news):
    """Авторизованному пользователю доступна форма для отправки комментария."""
    url = reverse('news:detail', args=[news.pk])
    response = author_client.get(url)
    assert 'form' in response.context
