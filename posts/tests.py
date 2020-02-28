from django.core import mail
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Post, Group
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.forms import PostForm
import time
User = get_user_model()


class EmailTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = self.client.post('/auth/signup/', {'username': 'test', 'password1': 'Test2020', 'password2':'Test2020', 'email': 'test@test.me'})
        self.user = User.objects.get(username='test')
        self.group = Group.objects.create(title='Группа', slug='slug', description='описание')
        
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.image = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
        self.post = Post.objects.create(group= self.group, text='Текст Поста', author = self.user, image = self.image)

    def testMail(self):
        self.assertEqual(len(mail.outbox), 1)

    def testMailSubject(self): 
        self.assertEqual(mail.outbox[0].subject, 'Подтверждение регистрации Yatube')

    def testProfile(self):
        response = self.client.get("/test/")
        self.assertEqual(response.status_code, 200)

    def test_authenticated(self):
        response = self.client.post('/auth/login/', {'username': 'test', 'password': 'Test2020'})
        response2 = self.client.get("/new/")
        self.assertEqual(response2.status_code, 200)

    def test_NOT_authenticated(self):
        response = self.client.get("/new/")
        self.assertEqual(response.status_code, 302)

    def testPost(self):
        response = self.client.get("/test/")
        response2 = self.client.get("/")
        response3 = self.client.get(f"/test/{self.post.id}/")
        self.assertContains(response, 'Текст Поста', count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response2, 'Текст Поста', count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response3, 'Текст Поста', count=None, status_code=200, msg_prefix='', html=False)

    def test_authenticatedEdit(self):
        response = self.client.post('/auth/login/', {'username': 'test', 'password': 'Test2020'})
        response = self.client.post(reverse('post_edit', kwargs={'username': 'test', 'post_id':self.post.id}),{'text': 'Новый текст поста'})
        time.sleep(20)
        response1 = self.client.get("/")
        response2 = self.client.get("/test/")
        response3 = self.client.get(f"/test/{self.post.id}/")
        self.assertContains(response1, 'Новый текст поста', count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response2, 'Новый текст поста', count=None, status_code=200, msg_prefix='', html=False)
        self.assertContains(response3, 'Новый текст поста', count=None, status_code=200, msg_prefix='', html=False)
        
    def test_404(self):
        response = self.client.get("/what_is_it/")
        self.assertEqual(response.status_code, 404)

    def test_img(self):
        response1 = self.client.get("/")
        response = self.client.get(f"/test/{self.post.id}/")
        response2 = self.client.get(f"/test/")
        response3 = self.client.get(f"/group/{self.group.slug}/")
        self.assertContains( response1, '<img', status_code=200 )
        self.assertContains( response2, '<img', status_code=200 )
        self.assertContains( response, '<img', status_code=200 )
        self.assertContains( response3, '<img', status_code=200 )
        with open('file.ext' , 'rb') as fp:
            form_data = {'author': self.user, 'text': 'Text', 'group': self.group, 'image': fp}
            form = PostForm(data=form_data)
            self.assertFalse(form.is_valid())

    def test_favorites(self):
        response = self.client.post(reverse('add_comment', kwargs={'username': 'test', 'post_id':self.post.id}),{'text': 'Новый комментарий'})
        self.assertNotContains( response, 'Новый комментарий', status_code=302 )
        response = self.client.post('/auth/login/', {'username': 'test', 'password': 'Test2020'})     
        response = self.client.get(reverse('profile_follow', kwargs={'username': 'test'}))
        self.assertContains( response, 'Вы не можете подписаться на самого себя!', status_code=200 )
        


        
        
