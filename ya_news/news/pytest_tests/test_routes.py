from http import HTTPStatus

import pytest

pytestmark = pytest.mark.django_db

HOME_URL = pytest.lazy_fixture("home_url")
DETAIL_URL = pytest.lazy_fixture("detail_url")
EDIT_URL = pytest.lazy_fixture("edit_url")
DELETE_URL = pytest.lazy_fixture("delete_url")
LOGIN_URL = pytest.lazy_fixture("login_url")
LOGOUT_URL = pytest.lazy_fixture("logout_url")
SIGNUP_URL = pytest.lazy_fixture("signup_url")

EDIT_REDIRECT_URL = pytest.lazy_fixture("edit_redirect_url")
DELETE_REDIRECT_URL = pytest.lazy_fixture("delete_redirect_url")

CLIENT_FIXTURE = pytest.lazy_fixture("client")
AUTHOR_CLIENT_FIXTURE = pytest.lazy_fixture("author_client")
ANOTHER_AUTHOR_CLIENT_FIXTURE = pytest.lazy_fixture("another_author_client")


@pytest.mark.parametrize(
    "url, client_fixture, expected_status, expected_redirect",
    [
        (HOME_URL, CLIENT_FIXTURE, HTTPStatus.OK, None),
        (DETAIL_URL, CLIENT_FIXTURE, HTTPStatus.OK, None),
        (LOGIN_URL, CLIENT_FIXTURE, HTTPStatus.OK, None),
        (LOGOUT_URL, CLIENT_FIXTURE, HTTPStatus.OK, None),
        (SIGNUP_URL, CLIENT_FIXTURE, HTTPStatus.OK, None),

        (EDIT_URL, AUTHOR_CLIENT_FIXTURE, HTTPStatus.OK, None),
        (DELETE_URL, AUTHOR_CLIENT_FIXTURE, HTTPStatus.OK, None),

        (EDIT_URL, ANOTHER_AUTHOR_CLIENT_FIXTURE, HTTPStatus.NOT_FOUND, None),
        (DELETE_URL, ANOTHER_AUTHOR_CLIENT_FIXTURE,
         HTTPStatus.NOT_FOUND, None),

        (EDIT_URL, CLIENT_FIXTURE, HTTPStatus.FOUND, EDIT_REDIRECT_URL),
        (DELETE_URL, CLIENT_FIXTURE, HTTPStatus.FOUND, DELETE_REDIRECT_URL),
    ],
)
def test_page_availability(url, client_fixture, expected_status,
                           expected_redirect):
    """Объединённый тест для проверки доступности страниц и редиректов."""
    response = client_fixture.get(url)

    assert response.status_code == expected_status

    # Если ожидается редирект, проверяем куда ведёт
    if expected_redirect:
        assert response.url == expected_redirect
