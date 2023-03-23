import unittest
from library import ext_api_interface
from unittest.mock import Mock
import requests
import json

class TestExtApiInterface(unittest.TestCase):
    def setUp(self):
        self.api = ext_api_interface.Books_API()
        self.book = "Learning Python (Learning)"
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests_data/json_data.txt', 'r') as f:
            self.json_data = json.loads(f.read())

    def test_make_request_True(self):
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        self.assertEqual(self.api.make_request(""), dict())

    def test_make_request_connection_error(self):
        ext_api_interface.requests.get = Mock(side_effect=requests.ConnectionError)
        url = "some url"
        self.assertEqual(self.api.make_request(url), None)

    def test_make_request_False(self):
        requests.get = Mock(return_value=Mock(status_code=100))
        self.assertEqual(self.api.make_request(""), None)

    def test_get_ebooks(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.assertEqual(self.api.get_ebooks(self.book), self.books_data)


    # ----------| My Tests |----------

    def test_is_book_available_with_available_book(self):
        self.api.make_request = Mock(return_value=self.json_data)
        result = self.api.is_book_available(self.book)
        self.assertTrue(result)

    def test_is_book_available_with_unavailable_book(self):
        self.api.make_request = Mock(return_value={'docs': []})
        result = self.api.is_book_available(self.book)
        self.assertFalse(result)

    def test_books_by_author_with_results(self):
        self.api.make_request = Mock(return_value=self.json_data)
        result = self.api.books_by_author('Fabrizio Romano')
        self.assertTrue("Learning Python (Learning)" in result)

    def test_books_by_author_with_no_results(self):
        self.api.make_request = Mock(return_value={'docs': []})
        result = self.api.books_by_author('Not an Author')
        self.assertListEqual(result, [])

    def test_is_book_available_no_results(self):
        self.api.make_request = Mock(return_value={"docs": []})
        self.assertFalse(self.api.is_book_available(self.book))

    def test_is_book_available_error(self):
        self.api.make_request = Mock(return_value=None)
        self.assertFalse(self.api.is_book_available(self.book))

    def test_books_by_author_no_results(self):
        self.api.make_request = Mock(return_value={"docs": []})
        self.assertEqual(self.api.books_by_author("Nonexistent Author"), [])

    def test_get_book_info_no_results(self):
        self.api.make_request = Mock(return_value={"docs": []})
        self.assertEqual(self.api.get_book_info(self.book), [])

    def test_get_book_info_error(self):
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.get_book_info(self.book), [])

    def test_get_ebooks_no_results(self):
        self.api.make_request = Mock(return_value={"docs": []})
        self.assertEqual(self.api.get_ebooks(self.book), [])

    def test_get_ebooks_error(self):
        self.api.make_request = Mock(return_value=None)
        self.assertEqual(self.api.get_ebooks(self.book), [])

    def test_get_book_info_with_all_fields(self):
        self.api.make_request = Mock(return_value={
            "docs": [{
                "title": "Test Book",
                "publisher": "Test Publisher",
                "publish_year": 2022,
                "language": "en"
            }]
        })
        expected_result = [{
            "title": "Test Book",
            "publisher": "Test Publisher",
            "publish_year": 2022,
            "language": "en"
        }]
        self.assertEqual(self.api.get_book_info("Test Book"), expected_result)

    def test_get_book_info_with_missing_fields(self):
        self.api.make_request = Mock(return_value={
            "docs": [{
                "title": "Test Book",
                "publish_year": 2022
            }]
        })
        expected_result = [{
            "title": "Test Book",
            "publish_year": 2022
        }]
        self.assertEqual(self.api.get_book_info("Test Book"), expected_result)

    def test_get_book_info_with_no_results(self):
        self.api.make_request = Mock(return_value={
            "docs": []
        })
        expected_result = []
        self.assertEqual(self.api.get_book_info("Nonexistent Book"), expected_result)

    def test_api_url(self):
        self.assertEqual(self.api.API_URL, "http://openlibrary.org/search.json")
    
    def test_request_url_construction(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.api.is_book_available(self.book)
        self.api.make_request.assert_called_with("http://openlibrary.org/search.json?q=Learning Python (Learning)")

    def test_is_book_available_with_exactly_one_book(self):
        self.api.make_request = Mock(return_value={'docs': [{'title': 'Single Book'}]})
        result = self.api.is_book_available('Single Book')
        self.assertTrue(result)

    def test_books_by_author_request_url_construction(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.api.books_by_author('Fabrizio Romano')
        self.api.make_request.assert_called_with("http://openlibrary.org/search.json?author=Fabrizio Romano")