import pytest

from django.urls import reverse

from http import HTTPStatus

from news.models import Comment

BAD_WORDS = ('редиска', 'негодяй')
WARNING = 'Не ругайтесь!'


def get_url(action, obj):
    """Сформировать URL для нужного действия с объектом."""
    return reverse(f'news:{action}', args=[obj.pk])


def post_request(client, action, obj, data=None):
    """Отправить POST-запрос и вернуть ответ."""
    return client.post(get_url(action, obj), data or {})


def test_anonymous_user_cannot_comment(client, news, comment_data):
    """Анонимный пользователь не может отправить комментарий."""
    response = post_request(client, 'detail', news, comment_data)

    assert Comment.objects.count() == 0
    assert response.status_code == HTTPStatus.FOUND


def test_authorized_user_can_comment(author_client, news, comment_data):
    """Авторизованный пользователь может отправить комментарий."""
    response = post_request(author_client, 'detail', news, comment_data)

    assert Comment.objects.count() == 1
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.parametrize("bad_word", BAD_WORDS)
def test_prohibited_words_in_comment(author_client, news, bad_word):
    """Запрещённые слова в комментариях не допускаются."""
    response = post_request(
        author_client,
        'detail',
        news,
        {'text': f'Это {bad_word}!'}
    )

    assert Comment.objects.count() == 0
    assert WARNING.encode() in response.content


def test_user_can_edit_own_comment(author_client, comment):
    """Авторизованный пользователь может редактировать свои комментарии."""
    new_text = "Обновленный комментарий"
    response = post_request(author_client, 'edit', comment, {'text': new_text})

    comment.refresh_from_db()
    assert comment.text == new_text
    assert response.status_code == HTTPStatus.FOUND


def test_user_cannot_edit_others_comment(author_client, another_user, comment):
    """Пользователь не может редактировать чужие комментарии."""
    author_client.force_login(another_user)
    response = post_request(
        author_client,
        'edit',
        comment,
        {'text': 'Мой новый текст'}
    )

    comment.refresh_from_db()
    assert comment.text != 'Мой новый текст'
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_user_can_delete_own_comment(author_client, comment):
    """Авторизованный пользователь может удалять свои комментарии."""
    response = post_request(author_client, 'delete', comment)

    assert not Comment.objects.filter(pk=comment.pk).exists()
    assert response.status_code == HTTPStatus.FOUND


def test_user_cannot_delete_others_comment(
        author_client,
        another_user,
        comment
):
    """Пользователь не может удалять чужие комментарии."""
    author_client.force_login(another_user)
    response = post_request(author_client, 'delete', comment)

    assert Comment.objects.filter(pk=comment.pk).exists()
    assert response.status_code == HTTPStatus.NOT_FOUND
