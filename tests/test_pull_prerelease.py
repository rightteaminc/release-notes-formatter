import unittest
from unittest.mock import patch, mock_open
import pull_prerelease 

class TestGitHubReleases(unittest.TestCase):

    @patch('requests.get')
    def test_get_draft_releases_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'draft': True, 'body': 'Test Draft Body'}]

        result = pull_prerelease.get_draft_releases('rightteaminc/parallax', 'dummy_token')
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0]['draft'])

    @patch('requests.get')
    def test_get_draft_releases_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = 'Not Found'

        result = pull_prerelease.get_draft_releases('rightteaminc/parallax', 'invalid_token')
        self.assertEqual(result, [])

    @patch('requests.get')
    def test_get_draft_releases_no_drafts(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'draft': False}]

        result = pull_prerelease.get_draft_releases('rightteaminc/parallax', 'dummy_token')
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_write_draft_to_file(self, mock_file):
        draft_release = {'body': 'Test Draft Content'}
        pull_prerelease.write_draft_to_file(draft_release, 'test.md')
        mock_file.assert_called_with('test.md', 'w')
        mock_file().write.assert_called_once_with('Test Draft Content')

# Replace with the actual name of your script
if __name__ == '__main__':
    unittest.main() 