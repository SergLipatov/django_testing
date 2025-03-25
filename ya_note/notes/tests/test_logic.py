from http import HTTPStatus
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
        response = self.client.post(ADD_URL, self.NEW_NOTE_DATA)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 3)  # + две стартовые
        new_note = Note.objects.get(slug=self.NEW_NOTE_DATA["slug"])
        self.assertEqual(new_note.title, self.NEW_NOTE_DATA["title"])
        self.assertEqual(new_note.text, self.NEW_NOTE_DATA["text"])
        self.assertEqual(new_note.author, self.author)

    def test_edit_note(self):
        """Автор может редактировать свою заметку."""
        self.EDIT_NOTE_DATA["slug"] = self.author_note.slug
        response = self.client.post(self.AUTHOR_EDIT_URL, self.EDIT_NOTE_DATA)
        self.assertRedirects(response, SUCCESS_URL)
        edited_note = Note.objects.get(slug=self.author_note.slug)
        self.assertEqual(edited_note.title, self.EDIT_NOTE_DATA["title"])
        self.assertEqual(edited_note.text, self.EDIT_NOTE_DATA["text"])

    def test_delete_note(self):
        """Автор может удалить свою заметку."""
        response = self.client.post(self.AUTHOR_DELETE_URL)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)  # Чужая остаётся

    def test_cannot_edit_other_user_note(self):
        """Пользователь НЕ может редактировать чужую заметку."""
        self.EDIT_NOTE_DATA["slug"] = self.other_user_note.slug
        response = self.client.post(self.OTHER_EDIT_URL, self.EDIT_NOTE_DATA)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        other_user_note = Note.objects.get(slug=self.other_user_note.slug)
        self.assertNotEqual(
            other_user_note.title,
            self.EDIT_NOTE_DATA["title"]
        )
        self.assertNotEqual(other_user_note.text, self.EDIT_NOTE_DATA["text"])

    def test_cannot_delete_other_user_note(self):
        """Пользователь НЕ может удалить чужую заметку."""
        response = self.client.post(self.OTHER_DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 2)
