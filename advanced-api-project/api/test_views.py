from django.test import TestCase
from django.urls import status
from . models import Book
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()

class BookViewSet(TestCase):
    def setUp(self):
        Book.objects.create(
            title="The Good day",
            author="Tunde",
            publication_year=2025
        )
        self.url = reverse('book-list')
        self.client = APIClient()
        
    def test_list_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_ok)
        self.assertEqual(len(response.data), 1)

    
class BookDetailViewSet(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="The Good day",
            author="Tunde",
            publication_year=2025
        )
        self.url = reverse('book-details', args=[self.book.id])

    def test_retrieve_book(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Good day')
        self.assertEqual(response.data['author'], 'Tunde')
        self.assertEqual(response.data['publication_year'], 2025)


    def test_non_existing_book(self):
        response = self.client.get(reverse('book-details', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
class BookCreateViewSet(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='smartuser', password='password12')
        self.url = reverse('book-list')
        self.valid_payload = {
            'title': 'The Good day',
            'author': 'Tunde',
            'publication_year': 2025
        }
        self.invalid_payload = {
            'title': '',
            'author': '',
            'publication_year': 2026
        }

    def test_create_valid_book(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_book(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
