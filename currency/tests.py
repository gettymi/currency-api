from django.test import TestCase, Client
from django.urls import reverse

class CurrencyApiTests(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_convert_valid(self):
        response = self.client.get('/api/convert/', {
            'from': 'USD',
            'to': 'EUR',
            'amount': 100
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('converted', response.json())

    def test_convert_missing_param(self):
        response = self.client.get('/api/convert/', {
            'from': 'USD',
            'to': 'EUR'
        })
        self.assertEqual(response.status_code, 400)

    def test_latest_valid(self):
        response = self.client.get('/api/latest/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('rates', response.json())

    def test_latest_with_symbols(self):
        response = self.client.get('/api/latest/', {
            'symbols': 'EUR,PLN'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('rates', response.json())

    def test_currencies(self):
        response = self.client.get('/api/currencies/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('USD', response.json())
