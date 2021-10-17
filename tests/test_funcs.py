import unittest
import ezvi.funcmodule as funcmodule
import ezvi.tools as tools

# Should probably use hypothesis if this gets any bigger.

to_write = {"insert":"i",
            "text":"foooo",
            "newline":"\n",
            "escape":chr(27)}

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
