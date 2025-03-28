from http import HTTPStatus

from .base import BaseTestCase
from .base import (
    LIST_URL, LOGIN_URL, SIGNUP_URL, LOGOUT_URL,
    REDIRECT_ADD_URL, REDIRECT_LIST_URL, REDIRECT_SUCCESS_URL,
    AUTHOR_DELETE_URL, AUTHOR_EDIT_URL, ADD_URL, SUCCESS_URL,
    REDIRECT_AUTHOR_EDIT_URL, REDIRECT_AUTHOR_DELETE_URL,
    AUTHOR_DETAIL_URL, REDIRECT_AUTHOR_DETAIL_URL, HOME_URL
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

    def test_all_routes_for_all_clients(self):
        """Проверка доступности всех основных страниц для разных клиентов."""
        public_urls = [SIGNUP_URL, LOGIN_URL, LOGOUT_URL, HOME_URL]
        clients = {
            'anonymous': self.client,
            'author': self.author_client,
            'reader': self.reader_client,
        }
        for client_name, client in clients.items():
            for url in public_urls:
                with self.subTest(client=client_name, url=url):
                    response = client.get(url)
                    self.assertEqual(
                        response.status_code,
                        HTTPStatus.OK,)