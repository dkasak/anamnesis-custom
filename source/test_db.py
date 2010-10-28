import db
import db_sqlite3fts
import config
import unittest

import os

class TestDatabase(unittest.TestCase):

	def setUp(self):
		self.db = db.get_instance()

	def tearDown(self):
		pass

	def __to_unicode(self, data):
		return [unicode(i) for i in data]

	def __insert_data(self, data):
		for i in range(len(data)):
			self.db.insert(data[i])

	def __compare_data(self, one, other):
		
		if len(one) == 0 and len(other) == 0:
			return
		
		self.assertEqual(one, list(zip(*other)[1]))

	def __insert_and_search(self, data):
		
		data = self.__to_unicode(data)
		self.__insert_data(data)
		
		values = self.db.search(len(data))
		values.reverse()
		
		self.__compare_data(data, values)

	def __insert_and_remove(self, data):
		
		data = self.__to_unicode(data)
		self.__insert_data(data)
		
		values = self.db.search(len(data))

		n = len(data)

		# for each inserted data
		for i in range(n):
			# remove it
			self.db.remove(values[i][0])

			# get data againt to make sure it was deleted
			new_values = self.db.search(n-i-1)
			new_values.reverse()
			self.__compare_data(data[:n-i-1], new_values)

			pair = self.db.search(1, values[i][1])
			if pair:
				self.assertNotEqual(values[i][0], pair[0][0])
				self.assertNotEqual(values[i][1], pair[0][1])
			

	def test_single_insert_and_search(self):
		self.__insert_and_search([u"a"])

	def test_insert_and_remove(self):
		self.__insert_and_remove([u"a", u"b", u"c"])

	def test_strip_spaces(self):
		self.__insert_and_search([u" bb "])

	def test_single_space(self):
		self.__insert_and_search([u" "])

	def __search_and_compare(self, keywords, data):
		self.__compare_data(data, self.db.search(len(data), keywords))

	def test_search_single_keyword(self):
		data = [u"hello, world!!", u"hi!", u"hey"]

		self.__insert_data(data)

		self.__search_and_compare("h", [u"hey", u"hi!", u"hello, world!!"])
		self.__search_and_compare("w", [u"hello, world!!"])
		self.__search_and_compare("he", [u"hey", u"hello, world!!"])
		self.__search_and_compare("hel", [u"hello, world!!"])
		self.__search_and_compare("hey", [u"hey"])
		self.__search_and_compare("hello", [u"hello, world!!"])
		self.__search_and_compare("hi", [u"hi!"])

	def test_search_multiple_keywords(self):
		data = [u"aa bb cc", u"aa bb dd", u"aa cc dd"]

		self.__insert_data(data)
		self.__search_and_compare("a b c", [u"aa bb cc"])
		self.__search_and_compare("a b d", [u"aa bb dd"])
		self.__search_and_compare("a c d", [u"aa cc dd"])
		self.__search_and_compare("b bb a", [u"aa bb dd", u"aa bb cc"])
		self.__search_and_compare("a c", [u"aa cc dd", u"aa bb cc"])
		self.__search_and_compare(" c a ", [u"aa cc dd", u"aa bb cc"])

	def test_insert_same_value(self):
		for i in range(5):
			self.db.insert(u"hello")
			self.db.insert(u"world")

		values = self.db.search(10)

		self.assertEqual(values[0][1], u"world")
		self.assertEqual(values[1][1], u"hello")

		for v in values[2:]:
			self.assertNotEqual(v[1], u"hello")
			self.assertNotEqual(v[1], u"world")

	def test_move_up(self):
		self.__insert_data([u"aa", u"bb", u"cc", u"dd", u"ee"])
		
		values = self.db.search(5)
		id = values[2][0]

		self.assertEqual(values[2][1], u"cc")
		self.db.move_up(id, u"cc")
		
		values = self.db.search(5)
		self.assertEqual(values[0][1], u"cc")
		for v in values[1:]:
			self.assertNotEqual(v[0], id)
			self.assertNotEqual(v[1], u"cc")

def test_implementation(implementation_name):
	print ("========================================")
	print ("============== Testing %s " % implementation_name)
	print ("========================================")
	suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabase)
	unittest.TextTestRunner(verbosity=2).run(suite)

def main():
	for clipboard_implementation in ["sqlite3fts"]:
		test_implementation(clipboard_implementation)

if __name__ == '__main__':
	
	main()

