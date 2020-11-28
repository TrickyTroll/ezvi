import unittest
import ez_vi.funcmodule as funcmodule

to_write = {"insert":"i",
            "text":"foooo", 
            "newline":"\n", 
            "text":"bar", 
            "escape":chr(27)}
                
class TestEncode(unittest.TestCase):
        
    def test_returns_dict(self):
        """
        Testing that the function returns a `dict`.
        """
        result = funcmodule.ez_encode(to_write)
        self.assertEqual(type(result),type({}))
        
    def test_encoded_chars(self):
        """
        Testing char chars have been encoded properly.
        """
        for key, value in to_write.items():
            assert type(value) == str
        result = funcmodule.ez_encode(to_write)                           
        for key, value in result.items():
            for item in value:
                self.assertIn(item.decode('utf-8'), to_write[key])
                self.assertEqual(type(item),type(''.encode('utf-8')))
        
if __name__ == '__main__':
    unittest.main()