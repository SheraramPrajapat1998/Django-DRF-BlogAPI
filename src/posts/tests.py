from django.utils import timezone
from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from posts.models import Post
from posts.api import views as posts_views
from django.contrib.auth import get_user_model
from django.utils.text import slugify
User = get_user_model()

post_title1 = 'Post Title 1'
post_slug1 = slugify(post_title1)
post_body1 = "Post Body 1"
username1 = 'testuser1'
userpassword1 = 'abc@123'
useremail1 = 'testuser1@gmail.com'


# Normal Inbuild TestCase
class PostTests(TestCase):
    @classmethod
    def setUp(cls):
        testuser1 = User.objects.create_user(
            username=username1, password=userpassword1)
        testuser1.save()
        test_post1 = Post.objects.create(
            title=post_title1, slug=post_slug1, author=testuser1, body=post_body1)
        test_post1.save()

    def test_post_blogpost_title_author_content(self):
        post1 = Post.objects.get(id=1)
        author = post1.author.username
        title = post1.title
        slug = post1.slug
        body = post1.body
        self.assertEqual(title, post_title1)
        self.assertEqual(body, post_body1)
        self.assertEqual(author, username1)
        self.assertEqual(slug, post_slug1)


# PyTest Library Test Cases
class BlogPostTests(APITestCase):
    def create_user_and_set_token_credentials(self):
        user = User.objects.create_user(username1, useremail1, userpassword1)
        token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {0}'.format(token.key))

    def post_blogpost(self, title, author, body, slug, status=Post.DRAFT, publish=timezone.now(), image=None):
        url = reverse(posts_views.PostListAPIView.name)
        data = {'title': title, 'author': author, 'body': body,
                'slug': slug, 'status': status, 'publish': publish, 'image': image}
        response = self.client.post(url, data=data, format='json')
        return response

    def test_post_and_get_blogpost(self):
        self.create_user_and_set_token_credentials()
        title = 'Blog Post Title 1'
        slug = slugify(title)
        author = User.objects.get(username=username1).username
        body = 'Blog Post Content 1'
        blogpost_status = Post.PUBLISHED
        response = self.post_blogpost(
            title, author, body, slug, blogpost_status)
        print("PK {0}".format(Post.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == 1
        saved_post = Post.objects.get()
        assert saved_post.title == title
        assert saved_post.slug == slug
        assert saved_post.body == body
        assert saved_post.status == blogpost_status if blogpost_status else Post.draft
        assert saved_post.author.username == author
        url = reverse(posts_views.PostDetailAPIView.name, None, {saved_post.pk})
        authorized_response = self.client.get(url, format='json')
        assert authorized_response.status_code == status.HTTP_200_OK
        assert authorized_response.data['title'] == title
        assert authorized_response.data['slug'] == slug
        assert authorized_response.data['body'] == body
        assert authorized_response.data['author'] == author
        assert authorized_response.data['status'] == blogpost_status if blogpost_status else Post.DRAFT

    def test_try_to_post_blogpost_without_author(self):
        title = 'Blog Post Title 1'
        slug = slugify(title)
        author = None
        body = 'Blog Post Content 1'
        blogpost_status = Post.PUBLISHED
        response = self.post_blogpost(
            title, author, body, slug, blogpost_status)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_existing_blogpost(self):
        self.create_user_and_set_token_credentials()
        title = 'Blog Post Title 1'
        slug = slugify(title)
        author = User.objects.get(username=username1).username
        body = 'Blog Post Content 1'
        blogpost_status = Post.PUBLISHED
        response1 = self.post_blogpost(
            title, author, body, slug, blogpost_status)
        assert response1.status_code == status.HTTP_201_CREATED
        response2 = self.post_blogpost(
            title, author, body, slug, blogpost_status)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_blogpost_collections(self):
        """
        Ensure we can retrieve the all bogpost collection
        """
        self.create_user_and_set_token_credentials()
        title = 'Blog Post Title 1'
        slug = slugify(title)
        author = User.objects.get(username=username1).username
        body = 'Blog Post Content 1'
        blogpost_status = Post.PUBLISHED
        self.post_blogpost(
            title, author, body, slug, blogpost_status)
        url = reverse(posts_views.PostListAPIView.name)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        # Make sure we retrieve only one item
        # NOTE: pagination must be set for below results
        assert response.data['count'] == 1
        response_data_result0 = response.data['results'][0]
        assert response_data_result0['title'] == title
        assert response_data_result0['slug'] == slug
        assert response_data_result0['body'] == body
        assert response_data_result0['status'] == blogpost_status if blogpost_status else Post.draft
        assert response_data_result0['author'] == author
