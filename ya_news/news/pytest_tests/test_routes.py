# test_routes.py
from http import HTTPStatus

import pytest
from django.urls import reverse


# Указываем в фикстурах встроенный клиент.
@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',  # Имя параметра функции.
    # Значения, которые будут передаваться в name.
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
# Указываем имя изменяемого параметра в сигнатуре теста.
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)  # Получаем ссылку на нужный адрес.
    response = client.get(url)  # Выполняем запрос.
    assert response.status_code == HTTPStatus.OK


def test_news_detail_page_availability(client, news):
    """Страница отдельной новости доступна анонимному пользователю."""
    url = reverse('news:detail', args=[news.pk])
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_edit_delete_comment_availability_for_author(author_client, comment):
    """Автор комментария может редактировать и удалять свой комментарий."""
    edit_url = reverse('news:edit', args=[comment.pk])
    delete_url = reverse('news:delete', args=[comment.pk])

    edit_response = author_client.get(edit_url)
    delete_response = author_client.get(delete_url)

    assert edit_response.status_code == HTTPStatus.OK
    assert delete_response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('url_name', ['news:edit', 'news:delete'])
def test_redirect_for_anonymous_user(client, comment, url_name):
    """Редирект анонима при попытке редактировать или удалить комментарий."""
    url = reverse(url_name, args=[comment.pk])
    response = client.get(url)

    expected_url = reverse('users:login') + f'?next={url}'
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == expected_url


@pytest.mark.parametrize('url_name', ['news:edit', 'news:delete'])
def test_edit_delete_comment_forbidden_for_other_users(author_client, comment,
                                                       another_user, url_name):
    """Пользователь не может редактировать или удалять чужие комментарии."""
    unauthorized_client = author_client
    unauthorized_client.force_login(another_user)

    url = reverse(url_name, args=[comment.pk])
    response = unauthorized_client.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND