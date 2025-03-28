from .base import BaseTestCase
from .base import LIST_URL, ADD_URL, AUTHOR_EDIT_URL
from notes.forms import NoteForm


class NoteContentTests(BaseTestCase):
    """Тесты контента страниц заметок."""

    def test_note_displayed_with_correct_fields(self):
        """Заметка автора отображается на странице с корректными данными."""
        response = self.author_client.get(LIST_URL)
        notes = response.context["object_list"]
        self.assertIn(self.note_by_author, notes)
        self.assertEqual(len(notes), 1)
        note = notes.get(pk=self.note_by_author.pk)
        self.assertEqual(note.title, self.note_by_author.title)
        self.assertEqual(note.text, self.note_by_author.text)
        self.assertEqual(note.slug, self.note_by_author.slug)
        self.assertEqual(note.author, self.note_by_author.author)

    def test_note_list_does_not_include_other_users_notes(self):
        """На странице списка заметок пользователя нет чужих заметок."""
        response = self.author_client.get(LIST_URL)
        notes = response.context["object_list"]
        self.assertNotIn(self.note_by_reader, notes)
        self.assertIn(self.note_by_author, notes)

    def test_create_edit_pages_have_correct_forms(self):
        """На страницах создания и редактирования есть форма NoteForm."""
        for url in [ADD_URL, AUTHOR_EDIT_URL]:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn("form", response.context)
                self.assertIsInstance(response.context["form"], NoteForm)
