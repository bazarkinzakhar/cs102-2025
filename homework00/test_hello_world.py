import unittest

from homework00 import hello_world


class HelloTestCase(unittest.TestCase):
    def test_hello(self):
        m = "Hello, world!"
        self.assertEqual(m, hello_world.text())
        
