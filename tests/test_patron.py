import unittest
from library import patron

class TestPatron(unittest.TestCase):

    def setUp(self):
        self.pat = patron.Patron('fname', 'lname', '20', '1234')

    def test_valid_name(self):
        pat = patron.Patron('fname', 'lname', '20', '1234')
        self.assertTrue(isinstance(pat, patron.Patron))

    def test_invalid_name(self):
        self.assertRaises(patron.InvalidNameException, patron.Patron, '1fname', '1lname', '20', '1234')
    
    def test_invalid_name_exception_string(self):
        with self.assertRaisesRegex(patron.InvalidNameException, '^Name should not contain numbers$'):
            patron.Patron('1fname', '1lname', '20', '1234')

    def test_invalid_name_fname(self):
        self.assertRaises(patron.InvalidNameException, patron.Patron, '1fname', 'lname', '20', '1234')

    def test_invalid_name_lname(self):
        self.assertRaises(patron.InvalidNameException, patron.Patron, 'fname', '1lname', '20', '1234')

    def test_add_borrowed_book_not_in(self):
        self.pat.add_borrowed_book("test1")
        self.assertEqual(self.pat.borrowed_books, ["test1"])

    def test_add_borrowed_book_in(self):
        self.pat.borrowed_books = ["test1"]
        self.pat.add_borrowed_book("test1")
        self.assertEqual(self.pat.borrowed_books, ["test1"])

    def test_get_borrowed_books(self):
        self.pat.borrowed_books = ["test1"]
        self.assertEqual(self.pat.get_borrowed_books(), ["test1"])

    def test_return_borrowed_book_in_list(self):
        self.pat.borrowed_books = ["test1"]
        self.pat.return_borrowed_book("test1")
        self.assertEqual(self.pat.borrowed_books, [])

    def test_return_borrowed_book_not_in_list(self):
        self.pat.borrowed_books = ["test1"]
        self.pat.return_borrowed_book("test2")
        self.assertEqual(self.pat.borrowed_books, ["test1"])

    def test_equal_true(self):
        same_patron = patron.Patron('fname', 'lname', '20', '1234')
        self.assertEqual(self.pat, same_patron)

    def test_equal_false(self):
        not_same_patron = patron.Patron('notfname', 'notlname', '40', '123456')
        self.assertNotEqual(self.pat, not_same_patron)

    def test_get_fname(self):
        self.assertEqual(self.pat.get_fname(), "fname")

    def test_get_lname(self):
        self.assertEqual(self.pat.get_lname(), "lname")

    def test_get_age(self):
        self.assertEqual(self.pat.get_age(), "20")

    def test_get_memberID(self):
        self.assertEqual(self.pat.get_memberID(), "1234")