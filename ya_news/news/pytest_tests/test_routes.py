import pytest
from http import HTTPStatus

pytestmark = pytest.mark.django_db

HOME_URL = pytest.lazy_fixture("home_url")
DETAIL_URL = pytest.lazy_fixture("detail_url")
EDIT_URL = pytest.lazy_fixture("edit_url")
DELETE_URL = pytest.lazy_fixture("delete_url")
LOGIN_URL = pytest.lazy_fixture("login_url")
LOGOUT_URL = pytest.lazy_fixture("logout_url")
SIGNUP_URL = pytest.lazy_fixture("signup_url")

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
        (EDIT_URL, ANOTHER_AUTHOR_CLIENT_FIXTURE, HTTPStatus.NOT_FOUND),
        (DELETE_URL, ANOTHER_AUTHOR_CLIENT_FIXTURE, HTTPStatus.NOT_FOUND),
        (LOGIN_URL, CLIENT_FIXTURE, HTTPStatus.OK),
        (LOGOUT_URL, CLIENT_FIXTURE, HTTPStatus.OK),
        (SIGNUP_URL, CLIENT_FIXTURE, HTTPStatus.OK),
    ],
)
def test_page_availability(url, client_fixture, expected_status):
    """Объединённый тест для проверки доступности страниц."""
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
