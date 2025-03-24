from django.conf import settings
from django.urls import reverse


def get_response(client, url_name, *args):
    """Вспомогательная функция для получения ответа."""
    url = reverse(url_name, args=args)
    return client.get(url)


def test_news_count_on_homepage(client, create_news):
    """Количество новостей на главной странице — не более 10."""
    response = get_response(client, 'news:home')
    assert len(response.context['object_list']) <= (
        settings.NEWS_COUNT_ON_HOME_PAGE
    )


def test_news_order(client, create_news):
    """Новости отсортированы от самой свежей к самой старой."""
    response = get_response(client, 'news:home')
    news_feed = response.context['object_list']
    news_dates = [news.date for news in news_feed]
    assert news_dates == sorted(news_dates, reverse=True)


def test_comments_order(client, news, create_comments):
    """Комментарии отсортированы в хронологическом порядке."""
    response = get_response(client, 'news:detail', news.pk)
    comments = response.context['news'].comment_set.all()
    comment_times = [comment.created for comment in comments]
    assert comment_times == sorted(comment_times)


def test_anonymous_client_has_no_form(client, news):
    """Анонимному пользователю недоступна форма для отправки комментария."""
    response = get_response(client, 'news:detail', news.pk)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news):
    """Авторизованному пользователю доступна форма для отправки комментария."""
    response = get_response(author_client, 'news:detail', news.pk)
    assert 'form' in response.context
