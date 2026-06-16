import unittest
from unittest.mock import MagicMock, patch
from src.pdf_loader import extract_text

class TestPDFLoader(unittest.TestCase):
    @patch("src.pdf_loader.PdfReader")
    def test_extract_text(self, mock_pdf_reader):
        # Setup mock reader and pages
        mock_reader_instance = MagicMock()
        
        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = "Page 1 content. "
        
        mock_page2 = MagicMock()
        mock_page2.extract_text.return_value = "Page 2 content."
        
        mock_reader_instance.pages = [mock_page1, mock_page2]
        mock_pdf_reader.return_value = mock_reader_instance
        
        text = extract_text("dummy.pdf")
        mock_pdf_reader.assert_called_once_with("dummy.pdf")
        self.assertEqual(text, "Page 1 content. Page 2 content.")

    @patch("src.pdf_loader.PdfReader")
    def test_extract_text_empty(self, mock_pdf_reader):
        mock_reader_instance = MagicMock()
        mock_page = MagicMock()
        mock_page.extract_text.return_value = None
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        text = extract_text("empty.pdf")
        self.assertEqual(text, "")

if __name__ == "__main__":
    unittest.main()
