import unittest
import ezvi.funcmodule as funcmodule
import ezvi.tools as tools

# Should probably use hypothesis if this gets any bigger.

to_write = {"insert":"i",
            "text":"foooo",
            "newline":"\n",
            "escape":chr(27)}

class TestEncode(unittest.TestCase):

    def test_returns_dict(self):
        """
        Testing that the function returns a `dict`.
        """
        result = tools.ez_encode_str(to_write)
        self.assertEqual(type(result),type({}))

    def test_encoded_chars(self):
        """
        Testing char chars have been encoded properly.
        """
        for key, value in to_write.items():
            self.assertEqual(type(value), type(""))
        result = tools.ez_encode_str(to_write)
        for key, value in result.items():
            for item in value:
                self.assertIn(item.decode('utf-8'), to_write[key])
                self.assertEqual(type(item),type(''.encode('utf-8')))

class TestEncodeStr(unittest.TestCase):

    def test_returns_list(self):
        """
        Testing that the function returns a `list`.
        """
        result = tools.ez_encode_str(to_write["text"]) # "foooo"
        self.assertEqual(type(result), type([]))

    def test_encoded_chars(self):
        """
        Testing that the list is encoded properly.
        """
        test_string = to_write["text"]
        result = tools.ez_encode_str(test_string) # "foooo"
        for i in range(len(result)):
            self.assertEqual(result[i].decode("utf-8"), test_string[i])

if __name__ == '__main__':
    unittest.main()
