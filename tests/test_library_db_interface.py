import unittest
from unittest.mock import Mock, call
from library import library_db_interface

class TestLibbraryDBInterface(unittest.TestCase):

    def setUp(self):
        self.db_interface = library_db_interface.Library_DB()

    def test_insert_patron_not_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=None)
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        self.db_interface.db.insert = Mock(return_value=10)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), 10)

    def test_update_patron(self):
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        db_update_mock = Mock()
        self.db_interface.db.update = db_update_mock
        self.db_interface.update_patron(Mock())
        db_update_mock.assert_called()

    def test_convert_patron_to_db_format(self):
        patron_mock = Mock()

        patron_mock.get_fname = Mock(return_value=1)
        patron_mock.get_lname = Mock(return_value=2)
        patron_mock.get_age = Mock(return_value=3)
        patron_mock.get_memberID = Mock(return_value=4)
        patron_mock.get_borrowed_books = Mock(return_value=5)
        self.assertEqual(self.db_interface.convert_patron_to_db_format(patron_mock),
                         {'fname': 1, 'lname': 2, 'age': 3, 'memberID': 4,
                          'borrowed_books': 5})

    #This purposefully isn't using a mock because this case is only reachable when Patron is None, and returns out immediately after
    def test_insert_patron_none(self):
        none_patron = None
        self.assertEqual(self.db_interface.insert_patron(none_patron), None)

    def test_insert_patron_already_in_db(self):
        patron_mock = Mock()
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.retrieve_patron = Mock(return_value=data)
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        self.db_interface.db.insert = Mock(return_value=None)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), None)

    def test_get_patron_count_one(self):
        db_mock = Mock()
        patron_data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        db_mock.all = Mock(return_value=[patron_data])
        self.db_interface.db.close() # close the open file before swapping out for mock
        self.db_interface.db = db_mock
        self.assertEqual(self.db_interface.get_patron_count(), 1)
        
    def test_get_patron_count_zero(self):
        self.assertEqual(self.db_interface.get_patron_count(), 0)

    def test_get_all_patrons_one(self):
        db_mock = Mock()
        patron_data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        db_mock.all = Mock(return_value=[patron_data])
        self.db_interface.db.close() # close the open file before swapping out for mock
        self.db_interface.db = db_mock
        self.assertEqual(self.db_interface.get_all_patrons(), [patron_data])

    def test_update_patron_none(self):
        none_patron = None
        self.assertEqual(self.db_interface.update_patron(none_patron), None)

    def test_close_db(self):
        db_mock = Mock()
        db_mock.close = Mock()
        self.db_interface.db.close() #close the actual db before swapping for a mock
        self.db_interface.db = db_mock
        self.db_interface.close_db()
        db_mock.close.assert_called()

    def test_retrieve_patron(self):
        patron_data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        db_mock = Mock()
        db_mock.search = Mock(return_value=[patron_data])
        self.db_interface.db.close() # close "real" db before swapping mock in
        self.db_interface.db = db_mock
        self.assertEqual(self.db_interface.retrieve_patron("memberID").__dict__, patron_data)

    def test_retrieve_patron_none(self):
        patron_data = None
        db_mock = Mock()
        db_mock.search = Mock(return_value=None)
        self.db_interface.db.close() # close "real" db before swapping mock in
        self.db_interface.db = db_mock
        self.assertEqual(self.db_interface.retrieve_patron("memberID"), patron_data)

    def test_db_filename(self):
        self.assertEqual(self.db_interface.DATABASE_FILE, 'db.json')