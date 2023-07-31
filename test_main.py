import re
import unittest
from main import replace_match, build_release_item_text

class TestReplaceMatch(unittest.TestCase):
    def test_replace_match(self):
        input_string = "- AB#1234 - some context about this pr"
        base_url = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'
        expected_output = "[AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234)"

        transformed_content = replace_match(re.search(r'(?<=- )AB[#-]?(\d+)', input_string), base_url)
        self.assertEqual(transformed_content, expected_output)

    def test_format_AB_with_hash(self):
        input_string = "- AB#1234 - some context about this pr"
        base_url = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'
        expected_output = "[AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234)"
        
        transformed_content = replace_match(re.search(r'(?<=- )AB[#-]?(\d+)', input_string), base_url)
        self.assertEqual(transformed_content, expected_output)

    def test_format_AB_with_hyphen(self):
        input_string = "- AB-1234-some context about this pr"
        base_url = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'
        expected_output = "[AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234)"
        
        transformed_content = replace_match(re.search(r'(?<=- )AB[#-]?(\d+)', input_string), base_url)
        self.assertEqual(transformed_content, expected_output)

    def test_already_formatted_link(self):
        input_string = "- AB#1234 - some context about this pr"
        base_url = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'
        expected_output = "[AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234)"
        
        transformed_content = replace_match(re.search(r'(?<=- )AB[#-]?(\d+)', input_string), base_url)
        self.assertEqual(transformed_content, expected_output)

class TestBuildReleaseItemText(unittest.TestCase):
    def test_build_final_content(self):
        input_string = "- AB#1234 - some context about this pr"
        base_url = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'
        expected_output = "- [AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234) - some context about this pr"

        transformed_content = build_release_item_text(input_string, base_url)
        self.assertEqual(transformed_content, expected_output)
    
    def test_format_AB_with_hash(self):
        input_string = "- AB#1234 - some context about this pr"
        base_url = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'
        expected_output = "- [AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234) - some context about this pr"

        transformed_content = build_release_item_text(input_string, base_url)
        self.assertEqual(transformed_content, expected_output)

    def test_format_AB_with_hyphen(self):
        input_string = "- AB-1234-some context about this pr"
        base_url = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'
        expected_output = "- [AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234) - some context about this pr"

        transformed_content = build_release_item_text(input_string, base_url)
        self.assertEqual(transformed_content, expected_output)

    def test_when_there_is_an_extra_space_between_ticket_and_content(self):
        input_string = "- AB#1234 -  some context about this pr"
        base_url = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'
        expected_output = "- [AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234) - some context about this pr"

        transformed_content = build_release_item_text(input_string, base_url)
        self.assertEqual(transformed_content, expected_output)

if __name__ == '__main__':
    unittest.main()
