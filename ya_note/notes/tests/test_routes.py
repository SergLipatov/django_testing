from http import HTTPStatus

from .base import BaseTestCase
from .base import (
    LIST_URL, ADD_URL, SUCCESS_URL, LOGIN_URL, SIGNUP_URL, LOGOUT_URL,
    REDIRECT_ADD_URL, REDIRECT_LIST_URL, REDIRECT_SUCCESS_URL,
    AUTHOR_DELETE_URL, AUTHOR_EDIT_URL, ADD_URL, SUCCESS_URL,
    REDIRECT_AUTHOR_EDIT_URL, REDIRECT_AUTHOR_DELETE_URL,
    AUTHOR_DETAIL_URL, REDIRECT_AUTHOR_DETAIL_URL
)


class TestRoutes(BaseTestCase):
    """Тесты доступности страниц."""

    def test_redirect_for_anonymous_users(self):
        """Анонимные пользователи перенаправляются на логин."""
        cases = {
            ADD_URL: REDIRECT_ADD_URL,
            LIST_URL: REDIRECT_LIST_URL,
            SUCCESS_URL: REDIRECT_SUCCESS_URL,
            AUTHOR_EDIT_URL: REDIRECT_AUTHOR_EDIT_URL,
            AUTHOR_DELETE_URL: REDIRECT_AUTHOR_DELETE_URL,
            AUTHOR_DETAIL_URL: REDIRECT_AUTHOR_DETAIL_URL,
        }

        for url, expected_redirect in cases.items():
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url),
                    expected_redirect
                )

    def test_auth_pages_available_for_everyone(self):
        """Страницы регистрации, входа и выхода доступны всем."""
        urls = [SIGNUP_URL, LOGIN_URL, LOGOUT_URL]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(
                    self.client.get(url).status_code,
                    HTTPStatus.OK
                )
