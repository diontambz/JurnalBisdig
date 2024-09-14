# Sistem Rekomendasi Jurnal Bisnis Digital


Selamat datang di Sistem Rekomendasi Jurnal Bisnis Digital! Proyek ini bertujuan untuk mempermudah proses menemukan jurnal bisnis digital terindex scopus yang relevan untuk keperluan penelitian dan akademis.
Dengan memanfaatkan teknik analisis teks canggih dan dataset komprehensif dari Scopus, sistem ini menyediakan rekomendasi jurnal yang akurat dan relevan.

### Apa Itu Sistem Ini?

Sistem Rekomendasi Jurnal Bisnis Digital adalah sebuah aplikasi web yang dirancang untuk membantu peneliti, akademisi, dan mahasiswa dalam menemukan jurnal yang paling sesuai dengan topik penelitian mereka. Sistem ini menggunakan algoritma pemrosesan bahasa alami (NLP) untuk menganalisis teks dari judul dan abstrak jurnal, kemudian mencocokkannya dengan kata kunci yang dimasukkan oleh pengguna.

### Tujuan

Tujuan utama dari sistem ini adalah untuk menghemat waktu dan usaha pengguna dalam mencari literatur penelitian yang relevan. Dengan memberikan rekomendasi yang tepat, sistem ini memungkinkan pengguna untuk lebih fokus pada aspek penting dari pekerjaan penelitian mereka.

### Teknologi yang Digunakan

- **Flask**: Kerangka kerja web untuk membangun aplikasi.
- **SQLAlchemy**: ORM untuk interaksi basis data.
- **Pandas**: Manipulasi dan analisis data.
- **scikit-learn**: Pustaka pembelajaran mesin untuk pemrosesan teks.
- **spaCy**: Pustaka pemrosesan bahasa alami.
- **NLTK**: Toolkit bahasa alami untuk pemrosesan teks.
- **Flask-Mail**: Penanganan email untuk fungsi reset kata sandi.
- **SQLite**: Basis data untuk menyimpan informasi pengguna dan penanda.

### Content Based Filtering

Sistem ini menggunakan pendekatan Content Based Filtering untuk memberikan rekomendasi jurnal. Teknik yang digunakan meliputi:

- **TF-IDF (Term Frequency-Inverse Document Frequency)**: Teknik ini digunakan untuk mengubah teks menjadi vektor numerik yang mencerminkan pentingnya kata-kata dalam dokumen.
- **Cosine Similarity**: Metode ini digunakan untuk mengukur kesamaan antara dua vektor teks. Dengan menghitung cosine similarity antara vektor kata kunci yang dimasukkan pengguna dan vektor jurnal dalam database, sistem dapat menemukan jurnal yang paling relevan.

## Fitur

- **Autentikasi Pengguna**: Registrasi, login, dan manajemen profil pengguna.
- **Rekomendasi Jurnal**: Masukkan kata kunci untuk menerima daftar rekomendasi jurnal berdasarkan kesamaan teks.
- **Penandaan (Bookmarking)**: Simpan dan kelola penanda untuk akses mudah ke artikel penting.
- **Reset Kata Sandi**: Reset kata sandi dengan aman melalui email.
- **Saran**: Kirimkan saran atau masukan untuk meningkatkan sistem.

## Screenshots:

