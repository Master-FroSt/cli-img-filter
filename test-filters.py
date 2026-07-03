import unittest
import numpy as np

# Mengimpor fungsi-fungsi dari file utama Anda
# Asumsi nama file utama adalah image_filters.py
from filters import (
    apply_invert,
    apply_brightness,
    apply_grayscale,
    apply_isolate_color
)


class TestImageFilters(unittest.TestCase):

    def setUp(self):
        """
        Dijalankan sebelum setiap test.
        Kita membuat "gambar" palsu berukuran 2x2 pixel dengan 3 channel (RGB).
        """
        self.test_image = np.array([
            [[255, 0, 0], [0, 255, 0]],  # Baris 1: Merah murni, Hijau murni
            [[0, 0, 255], [255, 255, 255]]  # Baris 2: Biru murni, Putih murni
        ], dtype=np.uint8)

    def test_apply_invert(self):
        """Test Invert: Hitam jadi putih, putih jadi hitam, warna dibalik."""
        result = apply_invert(self.test_image)

        # Expected: 255 - pixel
        expected = np.array([
            [[0, 255, 255], [255, 0, 255]],
            [[255, 255, 0], [0, 0, 0]]
        ], dtype=np.uint8)

        # Cek apakah hasilnya sama persis
        np.testing.assert_array_equal(result, expected)
        # Cek apakah tipe datanya tetap uint8
        self.assertEqual(result.dtype, np.uint8)

    def test_apply_brightness_clipping(self):
        """Test Brightness: Memastikan nilai tidak melebihi 255 (clip)."""
        # Meningkatkan kecerahan 100% (dikali 2.0)
        result = apply_brightness(self.test_image, percentage=100, is_lighten=True)

        # Merah murni [255, 0, 0] dikali 2 harusnya 510, tapi harus di-clip ke 255.
        expected_red_pixel = np.array([255, 0, 0], dtype=np.uint8)

        np.testing.assert_array_equal(result[0, 0], expected_red_pixel)
        self.assertEqual(result.dtype, np.uint8)

    def test_apply_grayscale(self):
        """Test Grayscale: Memastikan rumus dot product (Luminance) benar."""
        result = apply_grayscale(self.test_image)

        # Rumus: 0.2989*R + 0.5870*G + 0.1140*B
        # Untuk Merah [255, 0, 0] -> 255 * 0.2989 = 76.2195 -> dibulatkan 76
        expected_gray_val = 76

        # Karena ini grayscale, R, G, dan B harus memiliki nilai yang sama (76)
        expected_pixel = np.array([76, 76, 76], dtype=np.uint8)

        np.testing.assert_array_equal(result[0, 0], expected_pixel)
        # Cek apakah dimensi tetap (H, W, 3) meskipun abu-abu
        self.assertEqual(result.shape, self.test_image.shape)

    def test_apply_isolate_color(self):
        """Test Isolate Color: Memastikan channel yang tidak dipilih menjadi 0."""
        # Isolasi warna Biru (Channel B)
        result = apply_isolate_color(self.test_image, 'B (Biru)')

        # Pixel putih [255, 255, 255] harus menjadi [0, 0, 255]
        expected_pixel_from_white = np.array([0, 0, 255], dtype=np.uint8)
        np.testing.assert_array_equal(result[1, 1], expected_pixel_from_white)

        # Pixel merah [255, 0, 0] harus menjadi [0, 0, 0] karena tidak ada birunya
        expected_pixel_from_red = np.array([0, 0, 0], dtype=np.uint8)
        np.testing.assert_array_equal(result[0, 0], expected_pixel_from_red)


if __name__ == '__main__':
    unittest.main()