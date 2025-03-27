from .base import BaseTestCase
from .base import LIST_URL, ADD_URL, AUTHOR_EDIT_URL
from notes.forms import NoteForm


class NoteContentTests(BaseTestCase):
    """Тесты контента страниц заметок."""

    def test_note_list_contains_only_user_notes(self):
        """Список заметок содержит только заметки текущего пользователя."""
        response = self.author_client.get(LIST_URL)
        notes = response.context["object_list"]

        self.assertIn(self.note_by_author, notes)

        for note in notes:
            self.assertEqual(note.author, self.author)
            self.assertEqual(note.title, "Заметка автора")
            self.assertEqual(note.text, "Текст 1")
            self.assertEqual(note.slug, "author-note")

    def test_create_edit_pages_have_correct_forms(self):
        """На страницах создания и редактирования есть форма NoteForm."""
        for url in [ADD_URL, AUTHOR_EDIT_URL]:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn("form", response.context)
                self.assertIsInstance(response.context["form"], NoteForm)
