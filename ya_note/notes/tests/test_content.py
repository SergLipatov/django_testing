from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note  # Замените на вашу модель, если имя другое

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

    def setUp(self):
        """Осуществляем вход для user1 перед каждым тестом."""
        self.client.force_login(self.user1)

    def test_note_in_object_list(self):
        """Проверяем, что заметка передаётся в object_list в context."""
        response = self.client.get(
            reverse('notes:list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Проверяем, что в контексте есть object_list
        self.assertIn('object_list', response.context)

        # Проверяем, что note1 есть в object_list (записи пользователя user1)
        object_list = response.context['object_list']
        self.assertIn(self.note1, object_list)

    def test_notes_visibility(self):
        """Проверяем, что пользователь не видит чужие заметки."""
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        object_list = response.context['object_list']

        # Проверяем, что заметка user2 отсутствует в его списке
        self.assertNotIn(self.note2, object_list)

    def test_create_edit_forms(self):
        """Наличие формы на страницах создания и редактирования заметки."""
        # Проверяем страницу создания
        response_create = self.client.get(reverse('notes:add'))
        self.assertEqual(response_create.status_code, HTTPStatus.OK)
        self.assertIn('form',
                      response_create.context)  # Форма должна быть в контексте

        # Проверяем страницу редактирования
        response_edit = self.client.get(
            reverse('notes:edit', args=[self.note1.slug]))
        self.assertEqual(response_edit.status_code, HTTPStatus.OK)
        self.assertIn('form',
                      response_edit.context)
