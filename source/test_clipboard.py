import clipboard
import clipboard_gtk
import clipboard_gtk_xclip
import config
import unittest

import gtk
import gobject

class TestClipboard(unittest.TestCase):

	def setUp(self):
		self.clipboard = clipboard.get_instance()
		self.clipboard.add_listener("primary", self.primary_listener)
		self.clipboard.add_listener("clipboard", self.clipboard_listener)
		self.data = { "primary" : "~~", "clipboard" : "~~~" }

	def tearDown(self):
		self.clipboard.remove_listener("primary", self.primary_listener)
		self.clipboard.remove_listener("clipboard", self.clipboard_listener)

	def primary_listener(self, data):
		self.data["primary"] = data

	def clipboard_listener(self, data):
		self.data["clipboard"] = data

	def test_can_write_to_primary_false(self):
		config.write_to_primary = False
		self.assertFalse(self.clipboard.can_write_to_selection("primary"))

	def test_can_write_to_primary_true(self):
		config.write_to_primary = True
		self.assertTrue(self.clipboard.can_write_to_selection("primary"))

	def test_can_write_to_clipboard_false(self):
		config.write_to_clipboard = False
		self.assertFalse(self.clipboard.can_write_to_selection("clipboard"))

	def test_can_write_to_clipboard_true(self):
		config.write_to_clipboard = True
		self.assertTrue(self.clipboard.can_write_to_selection("clipboard"))

	def test_can_read_from_primary_false(self):
		config.read_from_primary = False
		self.assertFalse(self.clipboard.can_read_from_selection("primary"))

	def test_can_read_from_primary_true(self):
		config.read_from_primary = True
		self.assertTrue(self.clipboard.can_read_from_selection("primary"))

	def test_can_read_from_clipboard_false(self):
		config.read_from_clipboard = False
		self.assertFalse(self.clipboard.can_read_from_selection("clipboard"))

	def test_can_read_from_clipboard_true(self):
		config.read_from_clipboard = True
		self.assertTrue(self.clipboard.can_read_from_selection("clipboard"))

	def write_and_read(self, type, strings):
		old_data = self.data[type]

		for data in strings:
			self.clipboard.write(data)

			if self.clipboard.can_write_to_selection(type) and self.clipboard.can_read_from_selection(type):
				self.assertEqual(self.data[type], data)
			else:
				self.assertEqual(self.data[type], old_data)

	def __set_configuration(self, read_from_primary, write_to_primary, read_from_clipboard, write_to_clipboard):
		config.read_from_primary = read_from_primary
		config.write_to_primary = write_to_primary
		config.read_from_clipboard = read_from_clipboard
		config.write_to_clipboard = write_to_clipboard

	def __test_write_and_read_selection(self, selection):
		strings = ["ab", " Hello!! "]
		self.write_and_read(selection, strings)

	def test_write_and_read_primary(self):
		self.__set_configuration(True, True, False, False)
		self.__test_write_and_read_selection("primary")

	def test_write_and_noread_primary(self):
		self.__set_configuration(True, False, False, False)
		self.__test_write_and_read_selection("primary")

	def test_nowrite_and_read_primary(self):
		self.__set_configuration(False, True, False, False)
		self.__test_write_and_read_selection("primary")

	def test_write_and_read_clipboard(self):
		self.__set_configuration(False, False, True, True)
		self.__test_write_and_read_selection("clipboard")

	def test_nowrite_and_read_clipboard(self):
		self.__set_configuration(False, False, True, False)
		self.__test_write_and_read_selection("clipboard")

	def test_write_and_noread_clipboard(self):
		self.__set_configuration(False, False, False, True)
		self.__test_write_and_read_selection("clipboard")

def test_implementation(implementation_name):
	print "========================================"
	print "============== Testing %s " % implementation_name
	print "========================================"
	suite = unittest.TestLoader().loadTestsFromTestCase(TestClipboard)
	unittest.TextTestRunner(verbosity=2).run(suite)

def run_gtk():
	for clipboard_implementation in ["gtk", "gtk_xclip"]:
		test_implementation(clipboard_implementation)

if __name__ == '__main__':
	run_gtk()


