from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .urls import get_redirect_url
from notes.models import Note

User = get_user_model()


class BaseTestCase(TestCase):
    """Базовый тестовый класс с фикстурами и вспомогательными методами."""

    @classmethod
    def setUpTestData(cls):
        """Создаёт пользователей один раз на весь класс (экономит ресурсы)."""
        cls.author = User.objects.create(username="author")

    def setUp(self):
        """Создаёт тестовые данные перед каждым тестом."""
        self.author_client = self.client_class()
        self.author_client.force_login(self.author)
        self.anonymous_client = self.client_class()

        self.author_note = Note.objects.create(
            title="Заметка автора",
            text="Текст 1",
            author=self.author,
            slug="author-note"
        )

        self.author_edit_url = reverse(
            "notes:edit",
            args=[self.author_note.slug]
        )
        self.author_delete_url = reverse(
            "notes:delete",
            args=[self.author_note.slug]
        )
        self.author_detail_url = reverse(
            "notes:detail",
            args=[self.author_note.slug]
        )

        self.redirect_author_edit_url = get_redirect_url(self.author_edit_url)
        self.redirect_author_delete_url = get_redirect_url(
            self.author_delete_url)
        self.redirect_author_detail_url = get_redirect_url(
            self.author_detail_url)

        self.new_note_data = {
            "title": "Новая заметка",
            "text": "Какой-то текст",
            "slug": "new-note",
        }

        self.edit_note_data = {
            "title": "Обновлённая заметка",
            "text": "Обновлённый текст",
        }
