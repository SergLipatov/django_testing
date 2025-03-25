from http import HTTPStatus

from .base import BaseTestCase
from .urls import HOME_URL, LIST_URL, ADD_URL, SUCCESS_URL, LOGIN_URL


class TestRoutes(BaseTestCase):
    """Тесты доступности страниц."""

    def test_pages_availability(self):
        """Проверяет доступность страниц для разных пользователей."""
        cases = [
            (None, HOME_URL, HTTPStatus.OK),
            (self.author, LIST_URL, HTTPStatus.OK),
            (self.author, ADD_URL, HTTPStatus.OK),
            (self.author, self.AUTHOR_DETAIL_URL, HTTPStatus.OK),
            (self.author, self.AUTHOR_EDIT_URL, HTTPStatus.OK),
            (self.author, self.AUTHOR_DELETE_URL, HTTPStatus.OK),
            (self.other_user, self.AUTHOR_DETAIL_URL, HTTPStatus.NOT_FOUND),
            (self.other_user, self.AUTHOR_EDIT_URL, HTTPStatus.NOT_FOUND),
            (self.other_user, self.AUTHOR_DELETE_URL, HTTPStatus.NOT_FOUND),
        ]

        for user, url, expected_status in cases:
            if user:
                self.client.force_login(user)
            with self.subTest(user=user, url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirect_for_anonymous_users(self):
        """Анонимные пользователи перенаправлены на страницу логина."""
        protected_urls = [
            ADD_URL,
            LIST_URL,
            SUCCESS_URL,
            self.AUTHOR_EDIT_URL,
            self.AUTHOR_DELETE_URL,
            self.AUTHOR_DETAIL_URL,
        ]
        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    f"{LOGIN_URL}?next={url}"
                )
