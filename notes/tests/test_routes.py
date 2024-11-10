from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note


User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
            slug='one_note'
        )


    def test_home_page(self):
        url = reverse('notes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    
    def test_pages_availability(self):
            # Создаём набор тестовых данных - кортеж кортежей.
            # Каждый вложенный кортеж содержит два элемента:
            # имя пути и позиционные аргументы для функции reverse().
            urls = (                
                ('notes:add', None),
                ('notes:list', None),
                ('notes:success', None),           
            )
            # Итерируемся по внешнему кортежу 
            # и распаковываем содержимое вложенных кортежей:
            for name, args in urls:
                with self.subTest(name=name):
                    # Передаём имя и позиционный аргумент в reverse()
                    # и получаем адрес страницы для GET-запроса:
                    self.client.force_login(self.author)
                    url = reverse(name, args=args)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, HTTPStatus.OK) 


    def test_availability_for_note_edit_and_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            # Логиним пользователя в клиенте:
            self.client.force_login(user)
            # Для каждой пары "пользователь - ожидаемый ответ"
            # перебираем имена тестируемых страниц:
            for name in ('notes:edit', 'notes:delete', 'notes:detail'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)


    def test_redirect_to_login(self):
        urls = (                
                ('notes:add', None),
                ('notes:list', None),
                ('notes:add', None),
                ('notes:detail', self.note.slug,),
                ('notes:edit', self.note.slug,),
                ('notes:delete', self.note.slug,),
            )
        
        login_url = reverse('users:login')
        # В цикле перебираем имена страниц, с которых ожидаем редирект:
        for name, arg in urls:
            with self.subTest(name=name):
                # Получаем адрес страницы редактирования или удаления комментария:
                if arg is None:
                    url = reverse(name)
                else:
                    url = reverse(name, args=(arg,))
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                # Проверяем, что редирект приведёт именно на указанную ссылку.
                self.assertRedirects(response, redirect_url) 


    def test_availability_auth_pages_for_all_users(self):
        # Создаём набор тестовых данных - кортеж кортежей.
        # Каждый вложенный кортеж содержит два элемента:
        # имя пути и позиционные аргументы для функции reverse().
        urls = (                
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),        
        )
        # Итерируемся по внешнему кортежу 
        # и распаковываем содержимое вложенных кортежей:
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK) 