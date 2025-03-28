from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

HOME_URL = reverse("notes:home")
ADD_URL = reverse("notes:add")
SUCCESS_URL = reverse("notes:success")
LIST_URL = reverse("notes:list")
LOGIN_URL = reverse("users:login")
LOGOUT_URL = reverse("users:logout")
SIGNUP_URL = reverse("users:signup")
AUTHOR_EDIT_URL = reverse("notes:edit", args=["author-note"])
AUTHOR_DELETE_URL = reverse("notes:delete", args=["author-note"])
AUTHOR_DETAIL_URL = reverse("notes:detail", args=["author-note"])
READER_EDIT_URL = reverse("notes:edit", args=["reader-note"])
READER_DELETE_URL = reverse("notes:delete", args=["reader-note"])
READER_DETAIL_URL = reverse("notes:detail", args=["reader-note"])


def get_redirect_url(destination_url):
    return f"{LOGIN_URL}?next={destination_url}"


REDIRECT_ADD_URL = get_redirect_url(ADD_URL)
REDIRECT_LIST_URL = get_redirect_url(LIST_URL)
REDIRECT_SUCCESS_URL = get_redirect_url(SUCCESS_URL)
REDIRECT_AUTHOR_EDIT_URL = get_redirect_url(AUTHOR_EDIT_URL)
REDIRECT_AUTHOR_DELETE_URL = get_redirect_url(AUTHOR_DELETE_URL)
REDIRECT_AUTHOR_DETAIL_URL = get_redirect_url(AUTHOR_DETAIL_URL)


class BaseTestCase(TestCase):
    """Базовый тестовый класс с фикстурами и вспомогательными методами."""

    @classmethod
    def setUpTestData(cls):
        """Создаёт пользователей один раз на весь класс (экономит ресурсы)."""
        cls.author = User.objects.create(username="author")
        cls.reader = User.objects.create(username="reader")
        cls.author_client = cls.client_class()
        cls.author_client.force_login(cls.author)
        cls.reader_client = cls.client_class()
        cls.reader_client.force_login(cls.reader)

        cls.note_by_author = Note.objects.create(
            title="Заметка автора",
            text="Текст 1",
            author=cls.author,
            slug="author-note"
        )

        cls.note_by_reader = Note.objects.create(
            title="Заметка читателя",
            text="Текст 2",
            author=cls.reader,
            slug="reader-note"
        )

        cls.form_data = {
            "title": "Новая заметка",
            "text": "Какой-то текст",
            "slug": "new-note",
        }
