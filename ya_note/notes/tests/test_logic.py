from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class NoteTests(TestCase):
    """Тесты для проверки работы CRUD-операций с заметками."""

    @classmethod
    def setUpTestData(cls):
        """Создаёт тестовых пользователей и их заметки."""
        cls.user1 = User.objects.create(username='user1')
        cls.user2 = User.objects.create(username='user2')

        cls.note1 = Note.objects.create(
            title='Заметка 1', text='Текст 1', author=cls.user1, slug='note-1'
        )
        cls.note2 = Note.objects.create(
            title='Заметка 2', text='Текст 2', author=cls.user2, slug='note-2'
        )

    def setUp(self):
        """Логиним user1 перед каждым тестом."""
        self.client.force_login(self.user1)

    def get_url(self, name, slug=None):
        """Формирует URL для переданного действия (add, edit, delete)."""
        return reverse(f'notes:{name}', args=[slug] if slug else [])

    def get_redirect_url(self):
        """Возвращает URL для редиректа после успешных действий."""
        return '/done/'  # Фактический URL после операций

    def test_authenticated_user_can_create_note(self):
        """Авторизованный пользователь может создать заметку."""
        data = {
            'title': 'Новая заметка',
            'text': 'Какой-то текст',
            'slug': 'new-note'
        }
        response = self.client.post(self.get_url('add'), data)
        self.assertRedirects(response, self.get_redirect_url())
        self.assertTrue(Note.objects.filter(slug='new-note').exists())

    def test_user_can_edit_own_note(self):
        """Пользователь может редактировать свою заметку."""
        new_data = {
            'title': 'Обновлённая заметка',
            'text': 'Обновлённый текст',
            'slug': self.note1.slug
        }
        response = self.client.post(
            self.get_url('edit', self.note1.slug),
            new_data
        )
        self.assertRedirects(response, self.get_redirect_url())

        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title, 'Обновлённая заметка')

    def test_user_can_delete_own_note(self):
        """Пользователь может удалить свою заметку."""
        response = self.client.post(self.get_url('delete', self.note1.slug))
        self.assertRedirects(response, self.get_redirect_url())
        self.assertFalse(Note.objects.filter(id=self.note1.id).exists())
