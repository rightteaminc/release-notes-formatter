import unittest
from unittest.mock import patch, MagicMock
import datetime
import count_tags_for_month

class TestGitHubTags(unittest.TestCase):

  @patch("count_tags_for_month.requests.get")
  def test_get_tags_success(self, mock_get):
    """Test get_tags() returns a list of tags when API response is valid."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"name": "v1.0.0", "commit": {"sha": "abc123"}},
        {"name": "v1.1.0", "commit": {"sha": "def456"}}
    ]
    mock_get.return_value = mock_response

    tags = count_tags_for_month.get_tags()
    self.assertEqual(len(tags), 2)
    self.assertEqual(tags[0]["name"], "v1.0.0")

  @patch("count_tags_for_month.requests.get")
  def test_get_tags_failure(self, mock_get):
    """Test get_tags() handles API failure correctly."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"message": "Internal Server Error"}
    mock_get.return_value = mock_response

    tags = count_tags_for_month.get_tags()
    self.assertEqual(tags, [])  # Expect an empty list on failure

if __name__ == "__main__":
    unittest.main()
