from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note
from pytils.translit import slugify

User = get_user_model()


class NoteTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Создаём тестовых пользователей и их заметки."""
        cls.user1 = User.objects.create_user(
            username='user1',
            password='pass1'
        )
        cls.user2 = User.objects.create_user(
            username='user2',
            password='pass2'
        )

        cls.note1 = Note.objects.create(
            title='Заметка 1',
            text='Текст 1',
            author=cls.user1,
            slug='note-1'
        )
        cls.note2 = Note.objects.create(
            title='Заметка 2',
            text='Текст 2',
            author=cls.user2,
            slug='note-2'
        )

    def setUp(self):
        """Осуществляем вход для user1 перед каждым тестом."""
        self.client.login(username='user1', password='pass1')

    def test_authenticated_user_can_create_note(self):
        """Авторизованный пользователь может создать заметку."""
        response = self.client.post(reverse('notes:add'), {
            'title': 'Новая заметка',
            'text': 'Какой-то текст',
            'slug': 'new-note'
        })
        self.assertEqual(response.status_code,
                         302)  # Должен быть redirect после успешного создания
        self.assertTrue(Note.objects.filter(slug='new-note').exists())

    def test_anonymous_user_cannot_create_note(self):
        """Анонимный пользователь НЕ может создать заметку."""
        self.client.logout()  # Разлогиниваем пользователя
        response = self.client.post(reverse('notes:add'), {
            'title': 'Анонимная заметка',
            'text': 'Текст',
            'slug': 'anon-note'
        })
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(Note.objects.filter(
            slug='anon-note').exists())  # Заметка не должна быть создана

    def test_note_slug_unique(self):
        """Проверяем, что нельзя создать две заметки с одинаковым slug."""
        response = self.client.post(reverse('notes:add'), {
            'title': 'Дубликат',
            'text': 'Тест',
            'slug': 'note-1'  # Уже существует
        })
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Note.objects.filter(slug='note-1').count(), 1)

    def test_note_slug_autogeneration(self):
        """Если slug не указан, он должен автоматически сгенерироваться."""
        response = self.client.post(reverse('notes:add'), {
            'title': 'Тест заголовка',
            'text': 'Тест текста',
        })
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        note = Note.objects.get(title='Тест заголовка')
        expected_slug = slugify(
            'Тест заголовка')[:100]  # Должен совпадать со slugify
        self.assertEqual(note.slug, expected_slug)

    def test_user_can_edit_own_note(self):
        """Пользователь может редактировать свою заметку."""
        response = self.client.post(
            reverse('notes:edit', args=[self.note1.slug]), {
                'title': 'Обновлённая заметка',
                'text': 'Обновлённый текст',
                'slug': self.note1.slug
            })
        self.assertEqual(response.status_code,
                         302)  # Проверяем редирект после сохранения

        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title,
                         'Обновлённая заметка')  # Проверяем, что обновилось

    def test_user_cannot_edit_others_note(self):
        """Пользователь не может редактировать чужую заметку."""
        response = self.client.post(
            reverse('notes:edit', args=[self.note2.slug]), {
                'title': 'Чужая заметка',
                'text': 'Новый текст',
                'slug': self.note2.slug
            })
        self.assertEqual(response.status_code, 404)  # Ожидаем ошибку доступа
        self.note2.refresh_from_db()

        # Убедимся, что чужая заметка **не изменилась**
        self.assertNotEqual(self.note2.title, 'Чужая заметка')

    def test_user_can_delete_own_note(self):
        """Пользователь может удалить свою заметку."""
        response = self.client.post(
            reverse('notes:delete', args=[self.note1.slug]))
        self.assertEqual(response.status_code, 302)  # Должен быть редирект

        # Проверяем, что заметка удалена
        self.assertFalse(Note.objects.filter(id=self.note1.id).exists())

    def test_user_cannot_delete_others_note(self):
        """Пользователь не может удалять чужие заметки."""
        response = self.client.post(
            reverse('notes:delete', args=[self.note2.slug]))
        self.assertEqual(response.status_code, 404)  # Доступ запрещён

        # Проверяем, что чужая заметка всё ещё на месте
        self.assertTrue(Note.objects.filter(id=self.note2.id).exists())
