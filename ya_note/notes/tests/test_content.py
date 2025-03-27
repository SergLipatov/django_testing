from .base import BaseTestCase
from .base import LIST_URL, ADD_URL, AUTHOR_EDIT_URL
from notes.forms import NoteForm


class NoteContentTests(BaseTestCase):
    """Тесты контента страниц заметок."""

    def test_note_list_contains_only_user_notes(self):
        """Список заметок содержит только заметки текущего пользователя."""
        response = self.author_client.get(LIST_URL)
        notes = response.context["object_list"]
        self.assertTrue(
            all(note.author == self.author for note in notes),)
        note = next((n for n in notes if n.slug == self.note_by_author.slug),
                    None)
        self.assertIsNotNone(note,)
        self.assertEqual(note.title, self.note_by_author.title)
        self.assertEqual(note.text, self.note_by_author.text)
        self.assertEqual(note.slug, self.note_by_author.slug)
        self.assertEqual(note.author, self.note_by_author.author)

    def test_create_edit_pages_have_correct_forms(self):
        """На страницах создания и редактирования есть форма NoteForm."""
        for url in [ADD_URL, AUTHOR_EDIT_URL]:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn("form", response.context)
                self.assertIsInstance(response.context["form"], NoteForm)
