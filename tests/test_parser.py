from unittest.mock import MagicMock
from core.parser import extract_title_and_url


def test_extract_title_and_url_match():
    mock_driver = MagicMock()
    elem = MagicMock()
    elem.text.strip.return_value = "Beck/Arnley 072-9999 Brake Master Cylinder"
    elem.get_attribute.return_value = "https://www.amazon.com/example"
    mock_driver.find_elements.return_value = [elem]

    result = extract_title_and_url(mock_driver, "072-9999")
    assert result is not None
    title, url = result
    assert "072-9999" in title
    assert url.startswith("https://")
