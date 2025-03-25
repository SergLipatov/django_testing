from django.contrib.auth import get_user_model
from django.test import TestCase
from notes.models import Note
from .urls import detail_url, edit_url, delete_url

User = get_user_model()


class BaseTestCase(TestCase):
    """Базовый тестовый класс с фикстурами и вспомогательными методами."""

    NEW_NOTE_DATA = {
        "title": "Новая заметка",
        "text": "Какой-то текст",
        "slug": "new-note"
    }

    EDIT_NOTE_DATA = {
        "title": "Обновлённая заметка",
        "text": "Обновлённый текст",
    }

    @classmethod
    def setUpTestData(cls):
        """Создаёт тестовых пользователей и их заметки."""
        cls.author = User.objects.create(username="author")
        cls.other_user = User.objects.create(username="other_user")

        cls.author_note = Note.objects.create(
            title="Заметка автора",
            text="Текст 1",
            author=cls.author,
            slug="author-note"
        )

        cls.other_user_note = Note.objects.create(
            title="Заметка другого пользователя",
            text="Текст 2",
            author=cls.other_user,
            slug="other-note"
        )

        cls.AUTHOR_DETAIL_URL = detail_url(cls.author_note.slug)
        cls.AUTHOR_EDIT_URL = edit_url(cls.author_note.slug)
        cls.AUTHOR_DELETE_URL = delete_url(cls.author_note.slug)
        cls.OTHER_DETAIL_URL = detail_url(cls.other_user_note.slug)
        cls.OTHER_EDIT_URL = edit_url(cls.other_user_note.slug)
        cls.OTHER_DELETE_URL = delete_url(cls.other_user_note.slug)

    def login_author(self):
        """Логинит пользователя-автора (self.author)."""
        self.client.force_login(self.author)
