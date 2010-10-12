import clipboard
import clipboard_gtk
import clipboard_gtk_xclip
import config
import time
import unittest

class TestClipboard(unittest.TestCase):

	def setUpClass(self):
		print "setUpClass"

	def setUp(self):
		self.clipboard = clipboard.get_instance()
		self.clipboard.add_listener("primary", self.primary_listener)
		self.clipboard.add_listener("clipboard", self.clipboard_listener)
		self.data = { "primary" : "~~", "clipboard" : "~~~" }

		config.write_to_primary = True
		config.write_to_clipboard = True
		self.clipboard.write("-- undefined --")

		time.sleep(0.05)

	def tearDown(self):
		self.clipboard.remove_listener("primary", self.primary_listener)
		self.clipboard.remove_listener("clipboard", self.clipboard_listener)

	def primary_listener(self, data):
		self.data["primary"] = data

	def clipboard_listener(self, data):
		self.data["clipboard"] = data

	def test_can_write_to_primary(self):
		config.write_to_primary = False
		self.assertFalse(self.clipboard.can_write_to_selection("primary"))

		config.write_to_primary = True
		self.assertTrue(self.clipboard.can_write_to_selection("primary"))

	def test_can_write_to_clipboard(self):
		config.write_to_clipboard = False
		self.assertFalse(self.clipboard.can_write_to_selection("clipboard"))

		config.write_to_clipboard = True
		self.assertTrue(self.clipboard.can_write_to_selection("clipboard"))

	def test_can_read_from_primary(self):
		config.read_from_primary = False
		self.assertFalse(self.clipboard.can_read_from_selection("primary"))

		config.read_from_primary = True
		self.assertTrue(self.clipboard.can_read_from_selection("primary"))

	def test_can_read_from_clipboard(self):
		config.read_from_clipboard = False
		self.assertFalse(self.clipboard.can_read_from_selection("clipboard"))

		config.read_from_clipboard = True
		self.assertTrue(self.clipboard.can_read_from_selection("clipboard"))

	def write_and_read(self, type, strings):
		old_data = self.data[type]

		for data in strings:
			self.clipboard.write(data)
			time.sleep(0.05)
			if self.clipboard.can_write_to_selection(type) and self.clipboard.can_read_from_selection(type):
				self.assertEqual(self.data[type], data)
			else:
				self.assertEqual(self.data[type], old_data)

	def test_write_and_read(self):
		strings = ["ab", " Hello!! "]

		config.write_to_primary = False
		self.write_and_read("primary", strings)

		config.write_to_primary = True
		self.write_and_read("primary", strings)

		config.write_to_clipboard = False
		self.write_and_read("clipboard", strings)

		config.write_to_clipboard = True
		self.write_and_read("clipboard", strings)

def test_implementation(implementation_name):
	print "========================================"
	print "============== Testing %s " % implementation_name
	print "========================================"
	suite = unittest.TestLoader().loadTestsFromTestCase(TestClipboard)
	unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
	for clipboard_implementation in ["gtk", "gtk_xclip"]:
		test_implementation(clipboard_implementation)

