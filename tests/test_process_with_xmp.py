import unittest
from unittest.mock import patch, mock_open, MagicMock

from resize_and_copy_files import process_image_with_xmp


class TestProcessImageWithXMP(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("tempfile.NamedTemporaryFile")
    @patch("os.remove")
    @patch("subprocess.run")
    @patch("__main__.compress_image")  # Заменить __main__ на имя модуля, если функция импортируется
    def test_process_image_with_xmp(
            self, mock_compress, mock_subprocess, mock_remove, mock_tempfile, mock_file
    ):
        # Setup
        input_path = "test.jpg"
        compressed_path = "test_compressed.jpg"
        xmp_temp_file = MagicMock()
        xmp_temp_file.name = "temp.xmp"
        mock_tempfile.return_value.__enter__.return_value = xmp_temp_file
        mock_compress.return_value = compressed_path

        # Run
        result = process_image_with_xmp(input_path)

        # Assert compress_image was called correctly
        mock_compress.assert_called_once_with(input_path)

        # Check that exiftool was called to extract and write xmp
        calls = [
            # extract xmp
            unittest.mock.call(["exiftool", "-xmp", "-b", input_path], stdout=unittest.mock.ANY, check=True),
            # write xmp
            unittest.mock.call(
                ["exiftool", "-overwrite_original", "-tagsFromFile=temp.xmp", "-xmp", compressed_path],
                check=True
            )
        ]
        mock_subprocess.assert_has_calls(calls, any_order=False)

        # Check that the temporary file was removed
        mock_remove.assert_called_once_with("temp.xmp")

        # Final output should be path to compressed image
        self.assertEqual(result, compressed_path)


if __name__ == "__main__":
    unittest.main()
