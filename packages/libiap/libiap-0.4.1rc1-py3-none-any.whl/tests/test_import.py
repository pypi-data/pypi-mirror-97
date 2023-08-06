import unittest

import libica


class TestImport(unittest.TestCase):

    def test_import(self):
        print("libica.VERSION: ", libica.VERSION)
        self.assertEqual(libica.VERSION, "0.5.0")
