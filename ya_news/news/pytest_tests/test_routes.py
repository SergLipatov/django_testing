import pytest
from http import HTTPStatus

pytestmark = pytest.mark.django_db

HOME_URL = pytest.lazy_fixture("home_url")
DETAIL_URL = pytest.lazy_fixture("detail_url")
EDIT_URL = pytest.lazy_fixture("edit_url")
DELETE_URL = pytest.lazy_fixture("delete_url")
LOGIN_URL = pytest.lazy_fixture("login_url")

CLIENT_FIXTURE = pytest.lazy_fixture("client")
AUTHOR_CLIENT_FIXTURE = pytest.lazy_fixture("author_client")
ANOTHER_AUTHOR_CLIENT_FIXTURE = pytest.lazy_fixture("another_author_client")


@pytest.mark.parametrize(
    "url, client_fixture, expected_status",
    [
        (HOME_URL, CLIENT_FIXTURE, HTTPStatus.OK),
        (DETAIL_URL, CLIENT_FIXTURE, HTTPStatus.OK),
        (EDIT_URL, AUTHOR_CLIENT_FIXTURE, HTTPStatus.OK),
        (DELETE_URL, AUTHOR_CLIENT_FIXTURE, HTTPStatus.OK),
    ]
)
def test_page_availability(url, client_fixture, expected_status):
    """Проверяем доступность страниц для различных пользователей."""
    response = client_fixture.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "url, expected_redirect",
    [
        (EDIT_URL, LOGIN_URL),
        (DELETE_URL, LOGIN_URL),
    ],
)
def test_redirect_for_anonymous_user(client, url, expected_redirect):
    """Анонимный пользователь должен быть перенаправлен на страницу логина."""
    response = client.get(url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f"{expected_redirect}?next={url}"


@pytest.mark.parametrize("url", [EDIT_URL, DELETE_URL])
def test_edit_delete_comment_forbidden_for_other_users(
        another_author_client, url):
    """Пользователь не может редактировать или удалять чужие комментарии."""
    response = another_author_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
