import unittest
from src.chunker import create_chunks

class TestChunker(unittest.TestCase):
    def test_create_chunks_exact(self):
        text = "abcdefghij"
        chunks = create_chunks(text, chunk_size=5)
        self.assertEqual(chunks, ["abcde", "fghij"])

    def test_create_chunks_uneven(self):
        text = "abcdefghij"
        chunks = create_chunks(text, chunk_size=3)
        self.assertEqual(chunks, ["abc", "def", "ghi", "j"])

    def test_create_chunks_empty(self):
        text = ""
        chunks = create_chunks(text, chunk_size=5)
        self.assertEqual(chunks, [])

if __name__ == "__main__":
    unittest.main()
