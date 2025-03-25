from http import HTTPStatus

from notes.forms import NoteForm
from .base import BaseTestCase
from .urls import LIST_URL, ADD_URL


class NoteContentTests(BaseTestCase):
    """Тесты контента страниц заметок."""

    def setUp(self):
        """Логиним автора перед тестами."""
        self.login_author()

    def test_note_list_contains_only_user_notes(self):
        """Список заметок содержит только заметки текущего пользователя."""
        response = self.client.get(LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        notes = response.context["object_list"]
        self.assertIn(self.author_note, notes)
        self.assertNotIn(self.other_user_note, notes)

    def test_create_edit_pages_have_correct_forms(self):
        """На страницах создания и редактирования есть форма NoteForm."""
        urls = [ADD_URL, self.AUTHOR_EDIT_URL]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertIn("form", response.context)
                self.assertIsInstance(response.context["form"], NoteForm)
