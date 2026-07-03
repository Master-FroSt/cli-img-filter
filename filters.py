import numpy as np

def apply_brightness(pixels, percentage, is_lighten=True):
    """Menerapkan efek terang atau gelap."""
    factor = (1.0 + (percentage / 100.0)) if is_lighten else (1.0 - (percentage / 100.0))
    return np.clip(pixels * factor, 0, 255).astype(np.uint8)


def apply_grayscale(pixels):
    """Grayscale murni menggunakan persepsi luminansi."""
    grayscale = np.dot(pixels[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
    return np.stack((grayscale, grayscale, grayscale), axis=2)


def apply_black_and_white(pixels, threshold):
    """Hitam putih mutlak berdasarkan nilai threshold."""
    grayscale = np.dot(pixels[..., :3], [0.2989, 0.5870, 0.1140])
    bw_2d = np.where(grayscale > threshold, 255, 0).astype(np.uint8)
    return np.stack((bw_2d, bw_2d, bw_2d), axis=2)


def apply_invert(pixels):
    """Membalikkan nilai RGB (Negatif)."""
    return 255 - pixels


def apply_isolate_color(pixels, channel_choice):
    """Menyisakan hanya satu channel warna (R, G, atau B)."""
    result = np.zeros_like(pixels)
    if channel_choice == 'R (Merah)':
        result[..., 0] = pixels[..., 0]
    elif channel_choice == 'G (Hijau)':
        result[..., 1] = pixels[..., 1]
    elif channel_choice == 'B (Biru)':
        result[..., 2] = pixels[..., 2]
    return result


def apply_erase_color(pixels, channel_choice):
    """Menghapus warna dominan."""
    result = pixels.copy()
    r, g, b = result[..., 0], result[..., 1], result[..., 2]

    if channel_choice == 'R (Merah)':
        mask = (r > g) & (r > b)
        result[mask, 0] = 0
    elif channel_choice == 'G (Hijau)':
        mask = (g > r) & (g > b)
        result[mask, 1] = 0
    elif channel_choice == 'B (Biru)':
        mask = (b > r) & (b > g)
        result[mask, 2] = 0
    return result


def apply_tint(pixels, tint_choice):
    """Mengaplikasikan campuran warna untuk efek seperti Sepia (kustom), Rosewood, Patina."""
    mix = np.dot(pixels[..., :3], [0.3, 0.6, 0.1])
    result = np.zeros_like(pixels, dtype=np.float64)

    if tint_choice == 'Sepia':
        result[..., 0], result[..., 1], result[..., 2] = mix, mix * 0.8, mix * 0.6
    elif tint_choice == 'Rosewood':
        result[..., 0], result[..., 1], result[..., 2] = mix * 0.9, mix * 0.3, mix * 0.4
    elif tint_choice == 'Patina':
        result[..., 0], result[..., 1], result[..., 2] = mix * 0.4, mix * 0.8, mix * 0.7

    return np.clip(result, 0, 255).astype(np.uint8)


def apply_duotone(pixels, combination):
    """Duotone (Terang-Gelap)."""
    mix = np.dot(pixels[..., :3], [0.3, 0.6, 0.1])
    mix_inv = 255.0 - mix
    result = np.zeros_like(pixels, dtype=np.float64)

    if combination == '(Mix, Mix, Invert)':
        result[..., 0], result[..., 1], result[..., 2] = mix, mix, mix_inv
    elif combination == '(Mix, Invert, Mix)':
        result[..., 0], result[..., 1], result[..., 2] = mix, mix_inv, mix
    elif combination == '(Invert, Mix, Mix)':
        result[..., 0], result[..., 1], result[..., 2] = mix_inv, mix, mix
    elif combination == '(Mix, Invert, Invert)':
        result[..., 0], result[..., 1], result[..., 2] = mix, mix_inv, mix_inv
    elif combination == '(Invert, Mix, Invert)':
        result[..., 0], result[..., 1], result[..., 2] = mix_inv, mix, mix_inv
    elif combination == '(Invert, Invert, Mix)':
        result[..., 0], result[..., 1], result[..., 2] = mix_inv, mix_inv, mix

    return np.clip(result, 0, 255).astype(np.uint8)


def apply_posterize(pixels, levels=4):
    """Mengurangi jumlah warna untuk menciptakan efek flat/blok warna."""
    factor = 255 / (levels - 1)
    bucket_size = 256 / levels
    posterized = np.floor(pixels / bucket_size) * factor
    return np.clip(posterized, 0, 255).astype(np.uint8)


def apply_sepia_standard(pixels):
    """Sepia menggunakan rumus matriks perkalian standar industri."""
    sepia_matrix = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    sepia = np.dot(pixels[..., :3], sepia_matrix.T)
    result = pixels.copy()
    result[..., :3] = np.clip(sepia, 0, 255)
    return result.astype(np.uint8)


def apply_vintage(pixels, gamma=1.2):
    """Efek vintage klasik: Boost warna merah, kurangi biru, dan aplikasi gamma correction."""
    result = pixels.copy().astype(np.float64)
    result[..., 0] = result[..., 0] * 1.1
    result[..., 2] = result[..., 2] * 0.9
    result = 255.0 * (result / 255.0) ** (1.0 / gamma)
    return np.clip(result, 0, 255).astype(np.uint8)


def apply_brightness_contrast(pixels, alpha=1.2, beta=10):
    """Penyesuaian linear matematika dari keseluruhan ruang warna."""
    result = pixels.astype(np.float64) * alpha + beta
    return np.clip(result, 0, 255).astype(np.uint8)


def apply_solarize(pixels, threshold=128):
    """Inversi parsial."""
    result = np.where(pixels > threshold, 255 - pixels, pixels)
    return result.astype(np.uint8)


def apply_monochrome_tint(pixels, theme='matrix'):
    """Memaksa gambar menjadi hitam-putih, lalu mewarnainya dengan satu warna pekat murni."""
    grayscale = np.dot(pixels[..., :3], [0.2989, 0.5870, 0.1140])
    result = np.zeros_like(pixels, dtype=np.float64)

    if theme == 'matrix':
        result[..., 0], result[..., 1], result[..., 2] = 0, grayscale * 1.2, 0
    elif theme == 'cyanotype':
        result[..., 0], result[..., 1], result[..., 2] = grayscale * 0.2, grayscale * 0.5, grayscale * 1.5
    elif theme == 'blood':
        result[..., 0], result[..., 1], result[..., 2] = grayscale * 1.5, 0, 0

    if pixels.shape[-1] == 4:
        result_rgba = np.zeros_like(pixels, dtype=np.float64)
        result_rgba[..., :3] = result[..., :3]
        result_rgba[..., 3] = pixels[..., 3]
        return np.clip(result_rgba, 0, 255).astype(np.uint8)

    return np.clip(result, 0, 255).astype(np.uint8)
