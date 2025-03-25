from notes.models import Note
from .base import BaseTestCase
from .urls import ADD_URL, SUCCESS_URL


class NoteCRUDTests(BaseTestCase):
    """Тесты CRUD-операций с заметками."""

    def setUp(self):
        """Логиним автора перед тестами."""
        self.login_author()

    def test_create_note(self):
        """Авторизованный пользователь может создать заметку."""
        data = {"title": "Новая заметка", "text": "Текст", "slug": "new-note"}
        response = self.client.post(ADD_URL, data)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertTrue(Note.objects.filter(slug="new-note").exists())
        new_note = Note.objects.get(slug="new-note")
        self.assertEqual(new_note.title, data["title"])
        self.assertEqual(new_note.text, data["text"])
        self.assertEqual(new_note.author, self.author)

    def test_edit_note(self):
        """Автор может редактировать свою заметку."""
        data = {
            "title": "Обновлённая",
            "text": "Обновлённый текст",
            "slug": self.author_note.slug
        }
        response = self.client.post(self.AUTHOR_EDIT_URL, data)
        self.assertRedirects(response, SUCCESS_URL)
        self.author_note.refresh_from_db()
        self.assertEqual(self.author_note.title, data["title"])
        self.assertEqual(self.author_note.text, data["text"])

    def test_delete_note(self):
        """Автор может удалить свою заметку."""
        response = self.client.post(self.AUTHOR_DELETE_URL)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertFalse(Note.objects.filter(id=self.author_note.id).exists())
