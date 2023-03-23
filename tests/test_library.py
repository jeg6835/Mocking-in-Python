import unittest
from unittest.mock import Mock
from library import library
import json

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.lib = library.Library()
        #self.books_data = [{'title': 'Learning Python', 'ebook_count': 3}, {'title': 'Learning Python (Learning)', 'ebook_count': 1}, {'title': 'Learning Python', 'ebook_count': 1}, {'title': 'Learn to Program Using Python', 'ebook_count': 1}, {'title': 'Aprendendo Python', 'ebook_count': 1}, {'title': 'Python Basics', 'ebook_count': 1}]
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())   

    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('learning python'))

    def test_get_ebooks_count(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_ebooks_count("learning python"), 8)

    def test_is_ebook_false(self):
        self.assertFalse(self.lib.is_ebook('not a book in the system'))

    def test_is_ebook_by_author_True(self):
        self.lib.api.books_by_author = Mock(return_value=["Learning Python"])
        self.assertTrue(self.lib.is_book_by_author("Python for Beginners", "Learning Python"))

    def test_is_ebook_by_author_False(self):
        self.lib.api.books_by_author = Mock(return_value=["Learning Python"])
        self.assertFalse(self.lib.is_book_by_author("Python for Beginners", "Learning Python WHAT????!?!?"))

    def test_get_languages_for_book(self):
        self.lib.api.get_book_info = Mock(return_value=[{'language': {'English', 'French', 'German'}}])
        
        language_set = self.lib.get_languages_for_book('learning python')
        self.assertTrue('English' in language_set)
        self.assertTrue('French' in language_set)
        self.assertTrue('German' in language_set)
        self.assertTrue(len(language_set) == 3)  

    def test_register_patron(self):
        fname = 'Larry'
        lname = 'Joe'
        age = 28
        memberID = 'testID'
        self.lib.db.insert_patron = Mock(return_value=memberID)
        self.assertEqual(self.lib.register_patron(fname, lname, age, memberID), memberID)    

    def test_is_patron_registered_true(self):
        memberID = 'testID'
        patron = Mock(return_value={})
        patron.get_memberID = Mock(return_value=memberID)
        self.lib.db.retrieve_patron = Mock(return_value=True)
        self.assertTrue(self.lib.is_patron_registered(patron)) 

    def test_is_patron_registered_false(self):
        memberID = 'testID'
        patron = Mock(return_value={})
        patron.get_memberID = Mock(return_value=memberID)
        self.lib.db.retrieve_patron = Mock(return_value=False)
        self.assertFalse(self.lib.is_patron_registered(patron)) 

    def test_borrow_book(self):
        patron = Mock()
        patron.add_borrowed_book= Mock()
        self.lib.db.update_patron = Mock(return_value=patron)
        self.assertEqual(self.lib.borrow_book('Test book', patron), None) 

    def test_return_borrow_book(self):
        patron = Mock()
        patron.add_borrowed_book = Mock()
        self.lib.db.update_patron = Mock(return_value=patron)
        self.assertEqual(self.lib.return_borrowed_book('Test Book', patron), None) 

    def test_is_book_borrowed_True(self):
        patron = Mock()
        patron.get_borrowed_books = Mock(return_value={'test book', 'test book 2'})
        self.assertTrue(self.lib.is_book_borrowed('Test Book', patron))

    def test_is_book_borrowed_False(self):
        patron = Mock()
        patron.get_borrowed_books = Mock(return_value={'test book', 'test book 2'})
        self.assertFalse(self.lib.is_book_borrowed('Test Book 3', patron))  

    def test_register_patron_already_in_database(self):
        fname = 'Larry'
        lname = 'Joe'
        age = 28
        memberID = 'testID'
        self.lib.db.insert_patron = Mock(return_value=memberID)
        self.assertNotEqual(self.lib.register_patron(fname, lname, age, memberID), None)   