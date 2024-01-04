import re
import unittest
from main import format_ticket_number_list, build_release_item_text

class TestFormatTicketNumberList(unittest.TestCase):
    def test_format_ticket_number_list(self):
        input_string = "- AB#1234 - some context about this pr"
        base_url = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'
        expected_output = "[AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234)"

        transformed_content = format_ticket_number_list(re.search(r'(?<=- )AB[#-]?(\d+)', input_string), base_url)
        self.assertEqual(transformed_content, expected_output)

    def test_format_AB_with_hash(self):
        input_string = "- AB#1234 - some context about this pr"
        base_url = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'
        expected_output = "[AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234)"

        transformed_content = format_ticket_number_list(re.search(r'(?<=- )AB[#-]?(\d+)', input_string), base_url)
        self.assertEqual(transformed_content, expected_output)

    def test_format_AB_with_hyphen(self):
        input_string = "- AB-1234-some context about this pr"
        base_url = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'
        expected_output = "[AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234)"

        transformed_content = format_ticket_number_list(re.search(r'(?<=- )AB[#-]?(\d+)', input_string), base_url)
        self.assertEqual(transformed_content, expected_output)

    def test_already_formatted_link(self):
        input_string = "- AB#1234 - some context about this pr"
        base_url = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'
        expected_output = "[AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234)"

        transformed_content = format_ticket_number_list(re.search(r'(?<=- )AB[#-]?(\d+)', input_string), base_url)
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

    # def test_when_there_are_multiple_tickets(self):
    #     input_string = "- AB#1234, AB#2345 -  some context about this pr"
    #     base_url = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'
    #     expected_output = "- [AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234), [AB#2345](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/2345) - some context about this pr"

    #     transformed_content = build_release_item_text(input_string, base_url)
    #     self.assertEqual(transformed_content, expected_output)

if __name__ == '__main__':
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestFormatTicketNumberList))
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestBuildReleaseItemText))
