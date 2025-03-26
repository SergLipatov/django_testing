from http import HTTPStatus

from .base import BaseTestCase
from .urls import (
    LIST_URL, ADD_URL, SUCCESS_URL, LOGIN_URL, SIGNUP_URL, LOGOUT_URL,
    REDIRECT_ADD_URL, REDIRECT_LIST_URL, REDIRECT_SUCCESS_URL
)


class TestRoutes(BaseTestCase):
    """Тесты доступности страниц."""

    def test_redirect_for_anonymous_users(self):
        """Анонимные пользователи перенаправляются на логин."""
        protected_urls = {
            ADD_URL: REDIRECT_ADD_URL,
            LIST_URL: REDIRECT_LIST_URL,
            SUCCESS_URL: REDIRECT_SUCCESS_URL,
            self.author_edit_url: self.redirect_author_edit_url,
            self.author_delete_url: self.redirect_author_delete_url,
            self.author_detail_url: self.redirect_author_detail_url,
        }

        for url, expected_redirect in protected_urls.items():
            with self.subTest(url=url):
                self.assertRedirects(
                    self.anonymous_client.get(url),
                    expected_redirect
                )

    def test_auth_pages_available_for_everyone(self):
        """Страницы регистрации, входа и выхода доступны всем."""
        urls = [SIGNUP_URL, LOGIN_URL, LOGOUT_URL]
        for url in urls:
            with self.subTest(url=url):
                response = self.anonymous_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
