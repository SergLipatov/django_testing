from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from http import HTTPStatus

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Пупкин')
        cls.reader = User.objects.create(username='Залупкин')
        cls.note = Note.objects.create(title='Заголовок', text='Текст',
                                       author=cls.author)

    def check_url_status(self, user, urls, expected_status):
        """Универсальная функция для проверки доступности страниц."""
        if user:
            self.client.force_login(user)
        for name, args in urls:
            with self.subTest(user=user, name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_pages_availability(self):
        """Проверяет доступность страниц, доступных всем пользователям."""
        public_urls = (
            ('notes:home', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        self.check_url_status(
            user=None,
            urls=public_urls,
            expected_status=HTTPStatus.OK
        )

    def test_availability_for_note_detail_edit_and_delete(self):
        """Тест доступа к заметкам для автора и другого пользователя."""
        note_urls = (
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:detail', (self.note.slug,)),
        )
        user_status_pairs = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in user_status_pairs:
            self.check_url_status(
                user=user,
                urls=note_urls,
                expected_status=status
            )

    def test_redirect_for_anonymous(self):
        """Проверяет редирект неавторизованных пользователей."""
        protected_urls = (
            ('notes:add', None),
            ('notes:detail', (self.note.slug,)),
            ('notes:success', None),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:list', None),
        )
        login_url = reverse('users:login')
        for name, args in protected_urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_availability_for_auth_users(self):
        """Тестирует доступность страниц для авторизованных пользователей."""
        auth_urls = (
            ('notes:add', None),
            ('notes:list', None),
            ('notes:success', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        for user in (self.author, self.reader):
            self.check_url_status(
                user=user,
                urls=auth_urls,
                expected_status=HTTPStatus.OK
            )
