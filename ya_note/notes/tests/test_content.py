from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class NoteTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Создаём тестовых пользователей и их заметки."""
        cls.user1 = User.objects.create(username='user1')
        cls.user2 = User.objects.create(username='user2')

        cls.note1 = Note.objects.create(
            title='Заметка 1',
            text='Текст 1',
            author=cls.user1
        )
        cls.note2 = Note.objects.create(
            title='Заметка 2',
            text='Текст 2',
            author=cls.user2
        )  # От другого юзера

        cls.list_url = reverse('notes:list')

    def setUp(self):
        """Осуществляем вход для user1 перед каждым тестом."""
        self.client.force_login(self.user1)

    def assert_status_and_context(self, response, key='object_list'):
        """Проверяет статус 200 и наличие ключа в context."""
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(key, response.context)
        return response.context[key]

    def test_note_in_object_list(self):
        """Проверяем, что заметка пользователя отображается в списке."""
        object_list = self.assert_status_and_context(
            self.client.get(self.list_url))
        self.assertIn(self.note1, object_list)

    def test_notes_visibility(self):
        """Проверяем, что пользователь не видит чужие заметки."""
        object_list = self.assert_status_and_context(
            self.client.get(self.list_url))
        self.assertNotIn(self.note2, object_list)

    def test_create_edit_forms(self):
        """Проверяем наличие формы на страницах заметок."""
        urls = [
            reverse('notes:add'),
            reverse('notes:edit', args=[self.note1.slug])
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertIn('form', response.context)
