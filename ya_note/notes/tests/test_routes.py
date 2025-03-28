from http import HTTPStatus

from .base import BaseTestCase, READER_EDIT_URL, READER_DELETE_URL
from .base import (
    LIST_URL, LOGIN_URL, SIGNUP_URL, LOGOUT_URL,
    REDIRECT_ADD_URL, REDIRECT_LIST_URL, REDIRECT_SUCCESS_URL,
    AUTHOR_DELETE_URL, AUTHOR_EDIT_URL, ADD_URL, SUCCESS_URL,
    REDIRECT_AUTHOR_EDIT_URL, REDIRECT_AUTHOR_DELETE_URL,
    AUTHOR_DETAIL_URL, REDIRECT_AUTHOR_DETAIL_URL, HOME_URL
)


class TestRoutes(BaseTestCase):
    """Тесты маршрутов."""

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
         """Проверка доступности всех маршрутов для разных клиентов."""
         test_cases = [
             (SIGNUP_URL, self.client, HTTPStatus.OK),
             (LOGIN_URL, self.client, HTTPStatus.OK),
             (HOME_URL, self.client, HTTPStatus.OK),
             (SIGNUP_URL, self.author_client, HTTPStatus.OK),
             (LOGIN_URL, self.author_client, HTTPStatus.OK),
             (HOME_URL, self.author_client, HTTPStatus.OK),
             (SIGNUP_URL, self.reader_client, HTTPStatus.OK),
             (LOGIN_URL, self.reader_client, HTTPStatus.OK),
             (HOME_URL, self.reader_client, HTTPStatus.OK),
             (ADD_URL, self.client, HTTPStatus.FOUND),
             (LIST_URL, self.client, HTTPStatus.FOUND),
             (SUCCESS_URL, self.client, HTTPStatus.FOUND),
             (AUTHOR_DETAIL_URL, self.client, HTTPStatus.FOUND),
             (AUTHOR_EDIT_URL, self.client, HTTPStatus.FOUND),
             (AUTHOR_DELETE_URL, self.client, HTTPStatus.FOUND),
             (READER_EDIT_URL, self.client, HTTPStatus.FOUND),
             (READER_DELETE_URL, self.client, HTTPStatus.FOUND),
             (SIGNUP_URL, self.client, HTTPStatus.OK),
             (LOGIN_URL, self.client, HTTPStatus.OK),
             (HOME_URL, self.client, HTTPStatus.OK),
             (SIGNUP_URL, self.author_client, HTTPStatus.OK),
             (LOGIN_URL, self.author_client, HTTPStatus.OK),
             (HOME_URL, self.author_client, HTTPStatus.OK),
             (SIGNUP_URL, self.reader_client, HTTPStatus.OK),
             (LOGIN_URL, self.reader_client, HTTPStatus.OK),
             (HOME_URL, self.reader_client, HTTPStatus.OK),
             (ADD_URL, self.client, HTTPStatus.FOUND),
             (LIST_URL, self.client, HTTPStatus.FOUND),
             (SUCCESS_URL, self.client, HTTPStatus.FOUND),
             (AUTHOR_DETAIL_URL, self.client, HTTPStatus.FOUND),
             (AUTHOR_EDIT_URL, self.client, HTTPStatus.FOUND),
             (AUTHOR_DELETE_URL, self.client, HTTPStatus.FOUND),
             (READER_EDIT_URL, self.client, HTTPStatus.FOUND),
             (READER_DELETE_URL, self.client, HTTPStatus.FOUND),
             (ADD_URL, self.author_client, HTTPStatus.OK),
             (LIST_URL, self.author_client, HTTPStatus.OK),
             (SUCCESS_URL, self.author_client, HTTPStatus.OK),
             (AUTHOR_DETAIL_URL, self.author_client, HTTPStatus.OK),
             (AUTHOR_EDIT_URL, self.author_client, HTTPStatus.OK),
             (AUTHOR_DELETE_URL, self.author_client, HTTPStatus.OK),
             (ADD_URL, self.reader_client, HTTPStatus.OK),
             (LIST_URL, self.reader_client, HTTPStatus.OK),
             (SUCCESS_URL, self.reader_client, HTTPStatus.OK),
             (READER_EDIT_URL, self.reader_client, HTTPStatus.OK),
             (READER_DELETE_URL, self.reader_client, HTTPStatus.OK),
             (READER_EDIT_URL, self.author_client, HTTPStatus.NOT_FOUND),
             (READER_DELETE_URL, self.author_client, HTTPStatus.NOT_FOUND),
             (AUTHOR_EDIT_URL, self.reader_client, HTTPStatus.NOT_FOUND),
             (AUTHOR_DELETE_URL, self.reader_client, HTTPStatus.NOT_FOUND),
             (AUTHOR_DETAIL_URL, self.reader_client, HTTPStatus.NOT_FOUND),

         ]
         for url, client, expected_status in test_cases:
             with self.subTest(url=url, client=client):
                 self.assertEqual(
                     client.get(url).status_code,
                     expected_status, )


