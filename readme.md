# Pembukaan
Image Filter merupakan aplikasi yang sudah umum di pengolahan gambar. Secara sederhana, manipulasi gambar dilakukan dengan mengubah nilai RGB antara 0-255 dari gambar sesuai aturan tertentu.

Aplikasi ini menggunakan Numpy untuk memanipulasi gambar. Dibuat dalam _command-line interface_, aplikasi menerima input gambar dan mengeluarkan output gambar terfilter.

## Link
File berisi [perubahan terbaru](docs/changelog.md) dari aplikasi ini.\
File berisi [pembahasan mendetail](docs/theory.md) terkait teknologi OCR dari sudut pandang penulis.
# Petunjuk instalasi
1. Clone direktori Github ini dengan perintah `git clone https://github.com/Master-FroSt/cli-img-filter.git` di cmd
2. Jalankan salah satu dari kode berikut untuk menginstall dependency
```
pip install pillow numpy questionary
pip install -r requirements.txt
```
# Petunjuk penggunaan
1. Jalankan file .bat untuk membuat window.
2. Pilih menu untuk memproses gambar, lalu pilih gambar dari File Explorer.
3. Pilih filter yang diinginkan, atur konfigurasi, lalu klik menu proses.
4. Gambar akan dihasilkan pada folder 'out'.
5. Gambar dapat diproses berulang atau pengguna dapat memilih gambar baru.
## Petunjuk filter
### Custom
- Brightness: mengatur cahaya gambar
- Grayscale: gambar monokrom abu-abu
- Black & White: gambar hitam putih
- Invert: gambar invers warna 
- Isolate Color: gambar grayscale dengan satu warna menonjol
- Erase Color: hapus satu warna
- Tint: gambar campuran warna spesifik {Sepia, Rosewood, Patina}
- Duotone: gambar monokrom dengan warna berbeda

### Template
- Posterize: Gambar warna flat  
- Sepia: Filter Sepia umum
- Vintage: Gambar lama
- Brightness & Contrast: gambar serasa HDR
- Monochrome Tint: gambar Hitam putih pekat