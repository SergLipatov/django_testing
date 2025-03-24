import pytest

from django.urls import reverse

from http import HTTPStatus


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
def test_pages_availability_for_anonymous_user(client, name):
    """Публичные страницы доступны анонимному пользователю."""
    response = client.get(reverse(name))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_news_detail_page_availability(client, news):
    """Страница отдельной новости доступна анонимному пользователю."""
    response = client.get(reverse('news:detail', args=[news.pk]))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize('url_name', ['news:edit', 'news:delete'])
def test_edit_delete_comment_availability_for_author(author_client, comment,
                                                     url_name):
    """Автор комментария может редактировать и удалять свой комментарий."""
    response = author_client.get(reverse(url_name, args=[comment.pk]))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize('url_name', ['news:edit', 'news:delete'])
def test_redirect_for_anonymous_user(client, comment, url_name):
    """Анонимный пользователь перенаправляется на страницу логина."""
    url = reverse(url_name, args=[comment.pk])
    expected_url = reverse('users:login') + f'?next={url}'
    response = client.get(url)

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == expected_url


@pytest.mark.django_db
@pytest.mark.parametrize('url_name', ['news:edit', 'news:delete'])
def test_edit_delete_comment_forbidden_for_other_users(author_client, comment,
                                                       another_user, url_name):
    """Нельзя редактировать или удалять чужие комментарии."""
    author_client.force_login(another_user)
    response = author_client.get(reverse(url_name, args=[comment.pk]))

    assert response.status_code == HTTPStatus.NOT_FOUND
